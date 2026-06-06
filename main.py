import logging
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agents.supervisor_agent import SupervisorAgent

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s  %(message)s")


def run():
    print("\n🧭  Macro Advisor — Phase 1 stub")
    print("    (escribe 'exit' para salir)\n")

    history = []

    while True:
        user_input = input("Tu pregunta: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break

        history.append(HumanMessage(content=user_input))
        result = SupervisorAgent().graph.invoke({"messages": history})

        last = result["messages"][-1].content
        print(f"\n🤖  {last}")

        history = result["messages"]


if __name__ == "__main__":
    load_dotenv()
    run()
