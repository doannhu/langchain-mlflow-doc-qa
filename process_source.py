import chainlit as cl
from typing import Tuple, List, Optional
from typing_extensions import Annotated
from chainlit.element import ElementBased

def process_source(answer, src, all_sources, docs) -> Tuple[Annotated[str, "answer"], Annotated[Optional[List[ElementBased]], "src_elements"]]:
        found_sources = []
        src_elements = []

        for source in src.split(","):
            src_name = src.strip().replace(".", "")
            try:
                index = all_sources.index(src_name)
            except ValueError:
                continue
            text = docs[index].page_content
            found_sources.append(src_name)
            src_elements.append(cl.Text(content=text, name=src_name))

        if found_sources:
            answer += f"\nSources: {', '.join(found_sources)}"
        else:
            answer += "\n No source found"

        return answer, src_elements