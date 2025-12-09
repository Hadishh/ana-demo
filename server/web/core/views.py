from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions, status, generics
from core.agents import graphiti_agent


class Neo4jGraphView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        limit = int(request.query_params.get("limit", 200))

        def fetch_graph(tx, limit):

            query = f"MATCH (n)-[r]->(m) RETURN n, r, m LIMIT {limit};"

            result = tx.run(query)

            nodes = {}
            rels = []

            for record in result:
                n = record["n"]
                r = record["r"]
                m = record["m"]

                n_id = n.id
                m_id = m.id

                if n_id not in nodes:
                    nodes[n_id] = {
                        "id": str(n_id),
                        "labels": list(n.labels),
                        "properties": dict(n),
                    }

                if m_id not in nodes:
                    nodes[m_id] = {
                        "id": str(m_id),
                        "labels": list(m.labels),
                        "properties": dict(m),
                    }

                rels.append(
                    {
                        "id": f"{n_id}-{m_id}-{r.type}",
                        "start": str(n_id),
                        "end": str(m_id),
                        "type": r.type,
                        "properties": dict(r),
                    }
                )

            return list(nodes.values()), rels

        with graphiti_agent.driver.session() as session:
            nodes, rels = session.execute_read(fetch_graph, limit)

        return Response(
            {"nodes": nodes, "relationships": rels}, status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):

        with graphiti_agent.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n;")

        return Response(
            {"detail": "Neo4j database cleared"},
            status=status.HTTP_200_OK,
        )
