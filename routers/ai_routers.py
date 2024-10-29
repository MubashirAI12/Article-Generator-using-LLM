from fastapi import Depends, FastAPI, status, APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import logging
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(name)s:%(levelname)s:%(message)s:%(funcName)s')
file_handler = logging.FileHandler('article_generator.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
app = FastAPI()
origins = ["*"]
load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("openai_key")
router = APIRouter()

class blogParams(BaseModel):
    topic: str
    keywords: list[str]
    language: str
    writing_style: str
    variants: int
    article_length: int 


llm_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


@router.post("/ai/write_article/")
async def generate_blog_using_keywords(article_parameters: blogParams):
    try:
        topic=article_parameters.topic
        keywords=article_parameters.keywords
        language=article_parameters.language
        writing_style=article_parameters.writing_style
        article_length=article_parameters.article_length
        variants=article_parameters.variants
        blog_template= """
        Write an article on the topic "{topic}". The article should incorporate the following keywords: {keywords}. 
        Write the article in {language} and adopt a {writing_style} tone throughout. 
        The article should be approximately {article_length} words long.

        """
        prompt = ChatPromptTemplate.from_template(blog_template)
        output_parser = StrOutputParser()
        chain = prompt | llm_model | output_parser
        chain_input_list=[]
        for i in range(0, variants):
            chain_input_list.append({"topic": topic, "keywords": keywords, "language": language, "writing_style": writing_style, "article_length": article_length })
        article= await chain.abatch(chain_input_list)
        logger.info("generated article successfully")
        return JSONResponse(content={"message": "Article Generated Successfully!", "data": {"article_list":article},"httpStatusCode": status.HTTP_200_OK}, status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.critical(e)
        return JSONResponse(content={"error": "Error while generating article"}, status_code=status.HTTP_400_BAD_REQUEST)

