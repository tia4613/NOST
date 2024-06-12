import os
import logging
import re
import json
import time
from .deepL_translation import translate_summary
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    FewShotChatMessagePromptTemplate,
)
from langchain.schema.runnable import RunnablePassthrough


def elements_generator(user_prompt):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.getenv("OPENAI_API_KEY"),
        max_tokens=800,
        temperature=0.8,
    )

    examples = [
        {
            "user_prompt": "",
            "answer": """
                Title: The Wounded Ones
                Genre: Romantic Thriller
                Theme: Love and Discrimination
                Tone: Tense and Emotional
                Setting: Neo New York, 2156
                Characters:
                Eleanor Blackwood: A synthetic human rights advocate. Struggling to raise her two daughters after her husband was killed in an accident, Eleanor is an old friend of Frank Miller...
                Lydia Blackwood: Eleanor's oldest daughter, 17-year-old Lydia, has '94%' human DNA...
                Chloe Blackwood: Eleanor's youngest daughter, 12-year-old Chloe has '62%' human DNA...
                Frank Miller: A seasoned detective and journalist who exposes discrimination against synthetic humans and advocates for their equality...
            """,
        },
        {
            "user_prompt": "",
            "answer": """
                Title: Project-elven001
                Genre: Thriller, Science Fiction
                Theme: Ethics of Genetic Engineering, Exploitation, and Redemption
                Tone: Dark, Intense, and Realistic
                Setting: Near-future, Global Conflict Zones, Secret Laboratory
                Characters:
                Dr Viktor Hallstrom: A once-respected geneticist who has descended into madness, believing that creating elves is the pinnacle of genetic science...
                Lena: A 12-year-old war orphan with a strong spirit...
                Max: A 10-year-old boy with a keen intellect and innate curiosity...
                Sarah Collins: A top journalist who has assembled a team to produce a documentary about the dangers of war and the devastation of post-war areas...
            """,
        },
    ]

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{user_prompt}"),
            ("ai", "{answer}"),
        ]
    )

    example_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )

    elements_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an expert in fiction. Generate a detailed settings for a novel based on the following user input.
                Now create a setting(Title, Genre, Theme, Tone, Setting, Characters) for your novel, as shown in the examples.
                Character entries should only tell you about your character's personality and upbringing.Use “...” to separate them from other characters to make them more recognizable.
                Just tell me the answer to the input. Don't give interactive answers.
            """,
            ),
            (
                "assistant",
                "I'm an AI that generates the best fiction setting. Feel free to tell me anything about your fiction setting.",
            ),
            example_prompt,
            ("human", "{user_prompt}"),
        ]
    )

    elements_chain = elements_prompt | llm
    elements = elements_chain.invoke(
        {
            "user_prompt": user_prompt,  # user_prompt
        }
    )

    result_text = elements.content.strip()
    logging.debug(f"Synopsis Generator Response: {result_text}")

    try:
        result_lines = result_text.split("\n")
        data = {
            "title": "",
            "genre": "",
            "theme": "",
            "tone": "",
            "setting": "",
            "characters": "",
        }
        current_key = None
        for line in result_lines:
            line = line.strip()
            if line.startswith("Title:"):
                data["title"] = line.split("Title:", 1)[1].strip()
                current_key = "Title"
            elif line.startswith("Genre:"):
                data["genre"] = line.split("Genre:", 1)[1].strip()
                current_key = "Genre"
            elif line.startswith("Theme:"):
                data["theme"] = line.split("Theme:", 1)[1].strip()
                current_key = "Theme"
            elif line.startswith("Tone:"):
                data["tone"] = line.split("Tone:", 1)[1].strip()
                current_key = "Tone"
            elif line.startswith("Setting:"):
                data["setting"] = line.split("Setting:", 1)[1].strip()
                current_key = "Setting"
            elif line.startswith("Characters:"):
                data["characters"] = line.split("Characters:", 1)[1].strip()
                current_key = "Characters"
            elif current_key == "Characters":
                data["characters"] += " " + line

            data["characters"] = data["characters"].strip()

        return data
    except Exception as e:
        logging.error(f"Error parsing synopsis response: {e}")
        return {
            "title": "",
            "genre": "",
            "theme": "",
            "tone": "",
            "setting": "",
            "characters": "",
        }


def prologue_generator(elements):

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.getenv("OPENAI_API_KEY"),
        max_tokens=400,
        temperature=0.9,
    )

    examples = [
        {
            "setting": """
                "title": "The Royal Heart's Resolve",
                "genre": "Medieval Romance",
                "theme": "Love, Courage, and Resilience",
                "tone": "Romantic, Heartwarming, and Inspirational",
                "setting": "Kingdom of Avaloria, Medieval Europe",
                "characters": "Princess Elara: A kind-hearted and strong-willed princess who must navigate court politics and challenges to find true love and her own path. Prince Aldric: The brave and chivalrous prince from a neighboring kingdom, determined to win Princess Elara's heart and unite their kingdoms through love. Queen Isadora: Elara's regal and wise mother, who navigates the intrigues of court life while guiding her daughter through the challenges of royal duties and romance."
            """,
            "answer": """
                Prologue:
                The grand ballroom of the Ashford Manor was ablaze with candlelight, casting a warm glow over the assembled guests. The year was 1812, and the Regency era was in full swing. Ladies in exquisite gowns of silk and lace glided gracefully across the polished wooden floors, their laughter a soft murmur that blended with the strains of a delicate waltz played by the string quartet...Lady Eleanor Ashford, the eldest daughter of the Duke, stood at the edge of the room, her emerald eyes scanning the crowd. She wore a gown of deep burgundy, the color accentuating her fair complexion and the dark curls cascading down her back. Her heart raced as she spotted the tall, broad-shouldered figure of Lord Thomas Hamilton across the room...Thomas, the second son of the Earl of Westwood, had returned from the war just weeks earlier, his presence a welcome surprise to the ton. He was handsome, with dark hair and piercing blue eyes that seemed to hold a world of secrets. As their eyes met, a spark of recognition and longing passed between them, igniting an unspoken connection that neither could deny.
            """,
        },
    ]

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{setting}"),
            ("ai", "{answer}"),
        ]
    )

    example_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )

    prologue_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                    You are an expert in fiction.
                    You create only the prologue for your novel using the setting(Title, Genre, Theme, Tone, Setting, Characters) you've been given.
                    Prologue is a monologue or dialog that serves to set the scene and set the tone before the main story begins.
                    The novel is told from the point of view of one of the Characters.
                    Just tell me the answer to the input. Don't give interactive answers.
                    If there are no setting(Title, Genre, Theme, Tone, Setting, Characters) in the input, give a blank answer.
                """,
            ),
            example_prompt,
            ("human", "{setting}"),
        ]
    )

    prologue_chain = prologue_prompt | llm

    prologue = prologue_chain.invoke({"setting": elements})

    result_text = prologue.content.strip()

    try:
        result_lines = result_text.split("\n")
        data = {
            "prologue": "",
        }
        current_key = None
        for line in result_lines:
            if line.startswith("Prologue"):
                data["prologue"] = line.split("Prologue:", 1)[1].strip()
                current_key = "Prologue"
            elif current_key == "Prologue":
                data["prologue"] += " " + line

            data["prologue"] = data["prologue"].strip()

        return data
    except Exception as e:
        return e


def summary_generator(chapter_num, summary, elements, prologue, language):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"), temperature=1.2
    )

    memory = ConversationSummaryBufferMemory(
        llm=llm, max_token_limit=20000, memory_key="chat_history", return_messages=True
    )

    stages = [
        "writes Expositions that introduce the characters and setting of your novel and where events take place.",
        "writes Development which a series of events leads to conflict between characters.",
        "writes crises, where a reversal of events occurs, a new situation emerges, and the protagonist ultimately fails.",
        "writes a climax in which a solution to a new situation is realized, the protagonist implements it, and the conflict shifts.",
        "writes endings where the protagonist wraps up the case, all conflicts are resolved, and the story ends.",
    ]

    current_stage, next_stage = None, None

    for i in range(5):
        if (chapter_num-1)//6 == i:
            current_stage = stages[i]
            next_stage = stages[i+1] if chapter_num % 6 == 0 and i + \
                1 < len(stages) else stages[i]

    example_prompts = [
        {
            "summary": "Write a concise summary of the first chapter where the protagonist meets a mysterious informant.",
            "answer": """
                James Worthington prowled the fog-drenched streets of Victorian London. A note directed him to a secluded meeting. As he approached, a man in a long, dark coat emerged from the mist. The informant's voice was urgent: "They're watching, detective." He handed over a ledger filled with cryptic entries, urging James to uncover the truth before disappearing into the fog.
            """
        },
        {
            "summary": "Write a concise summary of the chapter where the protagonist faces their first major obstacle.",
            "answer": """
                James's investigation led him to Lord Blackwood's mansion. Disguised as a social call, he navigated the grand halls to find crucial evidence. As he rifled through drawers, Lord Blackwood entered. "What are you doing here, Worthington?" A tense exchange ensued, and James narrowly escaped, realizing Blackwood was onto him.
            """
        },
        {
            "summary": "Write a concise summary of the chapter where the protagonist discovers a shocking secret.",
            "answer": """
                In an abandoned library, James found letters from his late father, revealing a link to a criminal syndicate. The final letter detailed his father's regret and attempt to escape the syndicate. This revelation shook James, fueling his determination to bring the truth to light.
            """
        },
        {
            "summary": "Write a concise summary of the chapter where the protagonist forms an unexpected alliance.",
            "answer": """
                In a seedy tavern, James met Lila, a master thief. Initially tense, they formed an uneasy alliance. Lila's underworld knowledge and James's quest for truth aligned, and they planned to infiltrate the syndicate's stronghold together.
            """
        }
    ]

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{summary}"),
            ("ai", "{answer}"),
        ]
    )

    example_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=example_prompts,
    )

    summary_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""You are an experienced novelist who {{current_stage}}.
                Write a concise, character-focused summary of the next events in the story.
                Focus on the actions, decisions, and emotions of the characters.
                Avoid generic descriptions of suspense or tension.
                Ensure the summary flows smoothly from the prologue and adds new developments.
                """,
            ),
            example_prompt,
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{prompt}"),
        ]
    )

    recommend_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""
                You are an experienced novelist who {{next_stage}}.
                Based on the current summary prompt, provide three compelling recommendations for the next part of the summary.
                Be extremely contextual and realistic with your recommendations.
                Each recommendation should have 'Title': 'Description'. For example: 'James discovers a hidden clue': 'James finds a hidden compartment in the desk, revealing a map that leads to a secret location.'
                Limit the length of each description to 1-2 sentences.
                """,
            ),
            example_prompt,
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{current_story}"),
        ]
    ) if chapter_num <= 29 else None

    def load_memory():
        return memory.load_memory_variables({})["chat_history"]

    def parse_recommendations(recommendation_text):
        recommendations = []
        try:
            rec_lines = recommendation_text.split("\n")
            title, description = None, None
            for line in rec_lines:
                if line.startswith("Title:"):
                    if title and description:
                        recommendations.append(
                            {"Title": title, "Description": description}
                        )
                    title = line.split("Title:", 1)[1].strip()
                    description = None
                elif line.startswith("Description:"):
                    description = line.split("Description:", 1)[1].strip()
                    if title and description:
                        recommendations.append(
                            {"Title": title, "Description": description}
                        )
                        title, description = None, None
                if len(recommendations) == 3:
                    break
        except Exception as e:
            logging.error(f"Error parsing recommendations: {e}")

        return recommendations

    def generate_recommendations(chat_history, current_story, next_stage, language):
        if not recommend_template:
            return None

        formatted_recommendation_prompt = recommend_template.format(
            chat_history=chat_history,
            current_story=current_story,
            next_stage=next_stage,
        )
        logging.debug(f"Formatted Recommendation Prompt: {formatted_recommendation_prompt}")

        try:
            for attempt in range(3):
                recommendation_result = llm.invoke(
                    formatted_recommendation_prompt)
                logging.debug(f"Recommendation Result: {recommendation_result.content}")

                if recommendation_result.content:
                    recommendations = parse_recommendations(
                        recommendation_result.content)
                    if recommendations:
                        translated_recommendations = []
                        for rec in recommendations:
                            translated_title = translate_summary(
                                rec["Title"], language)
                            translated_description = translate_summary(
                                rec["Description"], language)
                            translated_recommendations.append({
                                "Title": translated_title,
                                "Description": translated_description,
                            })
                        return translated_recommendations
                logging.warning(f"Recommendation attempt {attempt + 1} failed, retrying...")
                time.sleep(1)

        except Exception as e:
            logging.error(f"Error generating recommendations: {e}")

        return None

    def remove_recommendation_paths(final_summary):
        pattern = re.compile(r"Recommended summary paths:.*$", re.DOTALL)
        cleaned_story = re.sub(pattern, "", final_summary).strip()
        return cleaned_story

    chat_history = load_memory()
    prompt = f"""
    Story Elements: {elements}
    Prologue: {prologue}
    Story Prompt: {summary}
    Previous Story: {chat_history}
    Write a concise, realistic, and engaging summary of the next events in the story. Highlight both hope and despair in the narrative. Make it provocative and creative.
    Ensure the summary continues smoothly from the prologue, without repeating information.
    Focus on new developments, character arcs, and plot progression.
    """
    formatted_final_prompt = summary_template.format(
        chat_history=chat_history, prompt=prompt, current_stage=current_stage
    )
    logging.debug(f"Formatted Final Prompt: {formatted_final_prompt}")
    result = llm.invoke(formatted_final_prompt)
    logging.debug(f"Summary Result: {result.content}")
    memory.save_context({"input": prompt}, {"output": result.content})

    cleaned_story = remove_recommendation_paths(result.content)
    cleaned_story = translate_summary(cleaned_story, language)
    recommendations = generate_recommendations(
        chat_history, result.content, next_stage, language
    )
    return {"final_summary": cleaned_story, "recommendations": recommendations}
