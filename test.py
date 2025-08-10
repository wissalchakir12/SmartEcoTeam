

import os
import feedparser
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.mistral import MistralChat
from agno.team.team import Team

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("⚠️ MISTRAL_API_KEY non défini dans .env")

RSS_FEED_URL = "http://feeds.reuters.com/reuters/businessNews"

class RSSCollectorAgent(Agent):
    def __init__(self):
        super().__init__()
        self.name = "RSSCollector"
        self.model = MistralChat(id="mistral-medium", api_key=api_key)

    def act(self, ctx):
        feed = feedparser.parse(RSS_FEED_URL)
        entries = feed.entries[:5]  # prendre les 5 derniers articles
        for entry in entries:
            title = entry.title
            summary = entry.summary
            content = f"{title}\n{summary}"
            print(f"[Collector] Article collecté: {title}")
            ctx.send("SummarizerAgent", {"content": content})

class SummarizerAgent(Agent):
    def __init__(self):
        super().__init__()
        self.name = "SummarizerAgent"
        self.model = MistralChat(id="mistral-medium", api_key=api_key)

    def act(self, ctx):
        msg = ctx.receive()
        if msg:
            content = msg.get("content", "")
            prompt = [
                {"role": "system", "content": "Tu es un assistant qui fait un résumé concis d'un article économique."},
                {"role": "user", "content": f"Résume ce contenu : {content}"}
            ]
            summary = self.model.chat(prompt)
            print(f"[Summarizer] Résumé: {summary}")
            ctx.send("AnalyzerAgent", {"summary": summary})

class AnalyzerAgent(Agent):
    def __init__(self):
        super().__init__()
        self.name = "AnalyzerAgent"
        self.model = MistralChat(id="mistral-medium", api_key=api_key)

    def act(self, ctx):
        msg = ctx.receive()
        if msg:
            summary = msg.get("summary", "")
            prompt = [
                {"role": "system", "content": "Tu es un analyste économique qui détecte tendances et risques."},
                {"role": "user", "content": f"Analyse ce résumé et donne tendances et risques : {summary}"}
            ]
            analysis = self.model.chat(prompt)
            print(f"[Analyzer] Analyse: {analysis}")
            ctx.send("RecommenderAgent", {"analysis": analysis})

class RecommenderAgent(Agent):
    def __init__(self):
        super().__init__()
        self.name = "RecommenderAgent"
        self.model = MistralChat(id="mistral-medium", api_key=api_key)
        self.recommendations = []

    def act(self, ctx):
        msg = ctx.receive()
        if msg:
            analysis = msg.get("analysis", "")
            prompt = [
                {"role": "system", "content": "Tu es un expert qui propose des recommandations stratégiques basées sur une analyse économique."},
                {"role": "user", "content": f"Propose des recommandations basées sur cette analyse : {analysis}"}
            ]
            recommendation = self.model.chat(prompt)
            print(f"[Recommender] Recommandation: {recommendation}")
            self.recommendations.append(recommendation)
            # Optionnel : ici tu peux stocker ou envoyer le rapport final

team = Team(
    name="EconomicNewsAnalysis",
    mode="coordinate",
    model=MistralChat(id="mistral-medium", api_key=api_key),
    members=[
        RSSCollectorAgent(),
        SummarizerAgent(),
        AnalyzerAgent(),
        RecommenderAgent(),
    ],
    instructions=[
        "Collaborez pour collecter, résumer, analyser et recommander sur les articles économiques.",
        "Présentez les résultats de façon claire et concise."
    ],
    show_members_responses=False,
    add_datetime_to_instructions=True,
)

if __name__ == "__main__":
    team.print_response(
        "Lancez l'analyse des derniers articles économiques.",
        stream=False,
        show_full_reasoning=False,
        stream_intermediate_steps=False,
    ) 