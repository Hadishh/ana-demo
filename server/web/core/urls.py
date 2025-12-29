from django.urls import path
from .views import Neo4jGraphView


urlpatterns = [path("graph/", Neo4jGraphView.as_view(), name="neo4j-graph")]
