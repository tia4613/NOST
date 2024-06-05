import os
import logging
import re
import json
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
        temperature=1.2,
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
            "user_prompt": "",  # 예시 넣어야 함
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
        max_tokens=800,
        temperature=1.2,
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
                The Kingdom of Avaloria lay bathed in the soft hues of dawn, a land steeped in tales of chivalry and courtly love. Within the stone walls of the castle, Princess Elara gazed out of her window, her mind heavy with the weight of her impending responsibilities. As the heir to the throne, she knew that her duty to her kingdom often overshadowed the desires of her own heart.
                In a neighboring kingdom, Prince Aldric prepared for his journey to Avaloria, his resolve unwavering as he sought to win the hand of Princess Elara. Their union was not just a matter of love but a beacon of hope for the two realms, a treaty sealed in the chambers of the heart.
                Meanwhile, Queen Isadora wandered the halls of the castle, her regal posture belying the concerns that knotted her brow. She had seen love kindle empires or extinguish them in a single breath. As the guiding light in her daughter's life, she vowed to protect Elara from the shadows that lurked within the castle walls.
                And so, against the backdrop of courtly intrigue and whispered secrets, the fates of Princess Elara, Prince Aldric, and Queen Isadora intertwined, bound by a destiny that only love, courage, and resilience could shape.
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


def summary_generator(chapter_num, summary):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"), temperature=1.2
    )

    memory = ConversationSummaryBufferMemory(
        llm=llm, max_token_limit=20000, memory_key="chat_history", return_messages=True
    )

    stage = [
        "writes Expositions that introduce the characters and setting of your novel and where events take place.",
        "writes Development which a series of events leads to conflict between characters.",
        "writes crises, where a reversal of events occurs, a new situation emerges, and the protagonist ultimately fails.",
        "writes a climax in which a solution to a new situation is realized, the protagonist implements it, and the conflict shifts.",
        "writes endings where the protagonist wraps up the case, all conflicts are resolved, and the story ends.",
    ]  # 발단, 전개, 위기, 절정, 결말

    current_stage, next_stage = None, None

    for i in range(4) :
        if (chapter_num-1)//3 == i :
            current_stage = stage[i]
            if chapter_num % 3 == 0 :
                next_stage = stage[i+1]
            elif chapter_num == 12 :    
                next_stage = None
            else :    
                next_stage = stage[i]
        
    summary_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an experienced novelist who {current_stage}. 
            Write a concise, realistic, and engaging summary based on the provided theme and previous context. 
            Develop the characters, setting, and plot with rich descriptions. 
            Ensure the summary flows smoothly, highlighting both hope and despair. 
            Make the narrative provocative and creative. 
            Avoid explicit reader interaction prompts or suggested paths.""",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{prompt}"),
        ]
    )
    if chapter_num <= 11:
        recommend_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                You are an experienced novelist who {next_stage}. 
                Based on the current summary prompt, provide three compelling recommendations for the next part of the summary.
                Your recommendations should highlight each of the starkly emotional and realistic choices: hope, tragedy, despair, depression, and enjoyment.
                Be extremely contextual and realistic with your recommendations. 
                Each recommendation should have 'Title': 'Description'. For example: 'Title': 'The Beginning of a Tragedy','Description': 'The people are kind to the new doctor in town, but under the guise of healing their wounds, the doctor slowly conducts experiments.' 
                The response format is exactly the same as the frames in the example.
                """,
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{current_story}"),
            ]
        )

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

    def generate_recommendations(chat_history, current_story, next_stage):
        if recommend_template:
            formatted_recommendation_prompt = recommend_template.format(
                chat_history=chat_history,
                current_story=current_story,
                next_stage=next_stage,
            )
            recommendation_result = llm.invoke(formatted_recommendation_prompt)
            recommendations = parse_recommendations(recommendation_result.content)
        else:
            recommendations = None
        return recommendations

    def remove_recommendation_paths(final_summary):
        pattern = re.compile(r"Recommended summary paths:.*$", re.DOTALL)
        cleaned_story = re.sub(pattern, "", final_summary).strip()
        return cleaned_story

    chat_history = load_memory()
    prompt = f"""
    Story Prompt: {summary}
    Previous Story: {chat_history}
    Write a concise, realistic, and engaging summary based on the above information. Highlight both hope and despair in the narrative. Make it provocative and creative.
    """

    formatted_final_prompt = summary_template.format(
        chat_history=chat_history, prompt=prompt, current_stage=current_stage
    )
    result = llm.invoke(formatted_final_prompt)
    memory.save_context({"input": prompt}, {"output": result.content})

    cleaned_story = remove_recommendation_paths(result.content)
    if chapter_num <= 11:
        recommendations = generate_recommendations(
            chat_history, result.content, next_stage)

        return {"final_summary": cleaned_story, "recommendations": recommendations}
    else:
        return {"final_summary": cleaned_story, "recommendations": None}
