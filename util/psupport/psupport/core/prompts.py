from textwrap import dedent
from typing import Callable, List, Tuple

from guidance import assistant, gen, system, user
from guidance.models import Model

# Patterns

## Run n times
def run_n_times(run : Callable[[], Model], n : int, answer_key : str) -> List[str]:
    results = []
    for i in range(1, n):
        r = run()
        results.append(r[answer_key])
    return results


## Run and then judge
def run_n_and_judge(model: Model, run : Callable[[], Model], n : int, answer_key : str, criteria : str) -> Tuple[str,str]:
    list = run_n_times(run, n, answer_key)
    with system():
        llm = model + dedent(f"""
         Can you please comment on the pros and cons of each of these options based on these criteria?
         ---
         Criteria:
         {criteria}
         ---
         """)
    with user():
       for i in range(0,len(list)):
            llm += dedent(f"""
                          ---
                          Option {i}:
                          {list[i]}
                        """)
    with assistant():
        llm += gen('thinking', temperature=0, max_tokens=2000)

    with user():
        llm += "Please return the text of the best option, based on the above thinking. Return just the text, not its option number."

    with assistant():
        llm += gen('answer', temperature=0, max_tokens=2000)

    return llm['answer'].strip(), str(llm)
