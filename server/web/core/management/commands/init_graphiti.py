# yourapp/management/commands/init_graphiti.py
import os
import asyncio

from django.core.management.base import BaseCommand
from graphiti_core import Graphiti


class Command(BaseCommand):
    help = "Initialize Graphiti indices and constraints in Neo4j"

    def handle(self, *args, **options):
        uri = os.environ.get("NEO4J_URI", "bolt://neo4j:7687")
        user = os.environ.get("NEO4J_USERNAME", "neo4j")
        password = os.environ.get("NEO4J_PASSWORD", "password")

        self.stdout.write(f"Connecting to Neo4j at {uri} as {user}...")

        graphiti = Graphiti(uri, user, password)

        build_fn = getattr(graphiti, "build_indices_and_constraints", None)
        if build_fn is None:
            raise SystemExit(
                "Graphiti client has no build_indices_and_constraints() method."
            )

        # Support both sync and async versions depending on graphiti-core version
        if asyncio.iscoroutinefunction(build_fn):
            asyncio.run(build_fn())
        else:
            build_fn()

        close_fn = getattr(graphiti, "close", None)
        if close_fn:
            if asyncio.iscoroutinefunction(close_fn):
                asyncio.run(close_fn())
            else:
                close_fn()

        self.stdout.write(
            self.style.SUCCESS("Graphiti indices & constraints initialized.")
        )
