import time
import dspy
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from typing import TypedDict, Annotated, List, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from typing import TypedDict, Annotated, List, Literal, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
import random
from datetime import datetime
from langgraph.graph.message import add_messages # ----> reducer

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

os.environ["GOOGLE_API_KEY"] = google_api_key
os.environ["TAVILY_API_KEY"] = tavily_api_key 

import dspy
lm = dspy.LM("gemini/gemini-2.0-flash", api_key=google_api_key)
dspy.configure(lm=lm)
dspy.configure_cache(
    enable_disk_cache=False,
    enable_memory_cache=False,
)

# Uncomment this to use mlflow
import mlflow
mlflow.autolog()
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Reflection")


class JokeIdea(BaseModel):
    setup: str
    contradiction: str
    punchline: str


class QueryToIdea(dspy.Signature):
    """
    You are a funny comedian and your goal is to generate a nice structure for a joke.

    """

    query: str = dspy.InputField()
    joke_idea: JokeIdea = dspy.OutputField()


class IdeaToJoke(dspy.Signature):
    """
    You are a funny comedian who likes to tell stories before delivering a punchline.
    You are always funny and act on the input joke idea.
    If you are provided a draft of a joke, your goal should to make it make it funnier and more punchy.
    """

    joke_idea: JokeIdea = dspy.InputField()
    joke_draft: Optional[str] = dspy.InputField(description="An existing joke that you need to either refine, or change")
    joke: str = dspy.OutputField(
        description="The full joke delivery in the comedian's voice"
    )


class JokeJudge(dspy.Signature):
    """Rank each joke idea between 1-N.
    Rank 1 is the most unique and funniest."""

    joke_idea: List[JokeIdea] = dspy.InputField()
    joke_ratings: List[int] = dspy.OutputField(description="Rank between 1, 2, 3 ... N")


def check_score_goodness(args, pred):
    num_samples = len(args["joke_idea"])
    same_length = len(pred.joke_ratings) == num_samples
    all_ranks_present = all([(i + 1) in pred.joke_ratings for i in range(num_samples)])
    return 1 if (same_length and all_ranks_present) else 0


class ConditionalJokeGenerator(dspy.Module):
    def __init__(self, num_samples=2, num_reflection_steps=2):
        self.query_to_idea = dspy.ChainOfThought(QueryToIdea)
        self.idea_to_joke = dspy.ChainOfThought(IdeaToJoke)
        self.judge = dspy.Refine(
            module=dspy.ChainOfThought(JokeJudge),
            N=3, reward_fn=check_score_goodness, threshold=1,
        )

        self.num_samples = num_samples
        self.num_reflection_steps = num_reflection_steps
        

    async def aforward(self, query: str):

        joke_ideas = await asyncio.gather(
            *[self.query_to_idea.aforward(query=query) for _ in range(self.num_samples)]
        )
        print("Generated Joke Ideas: \n", joke_ideas)

        judge_score = self.judge(joke_idea=joke_ideas).joke_ratings
        print("Judge Score for each: ", judge_score)

        best_joke_idea_idx = judge_score.index(1)
        selected_joke_idea = joke_ideas[best_joke_idea_idx]
        print("Selected Joke Idea: \n", selected_joke_idea)
        
        joke = None
        for _ in range(self.num_reflection_steps):
            joke = self.idea_to_joke(joke_idea=selected_joke_idea,
                                     joke_draft=joke)
            print(f"iteration: {_}: Joke: {joke}")
        return joke


async def main():
    joke_generator = ConditionalJokeGenerator()
    start_time = time.time()
    joke = await joke_generator.acall(
        query="Write a joke about AI that has to do with them turning rogue."
    )

    print("---")
    print(joke)
    print(time.time() - start_time)


if __name__ == "__main__":
    asyncio.run(main())