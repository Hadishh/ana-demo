from rest_framework import serializers

from neo4j.time import DateTime


class Neo4jDateTimeField(serializers.DateTimeField):

    def to_representation(self, value):
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return super().to_representation(value)


class PropertiesField(serializers.Serializer):

    def to_representation(self, properties_dict):
        safe_props = {}
        for key, value in properties_dict.items():
            if "embedding" in key:
                print("continued")
                continue
            if isinstance(value, DateTime):
                safe_props[key] = Neo4jDateTimeField().to_representation(value)
            else:
                safe_props[key] = value

        return safe_props


class NodeSerializer(serializers.Serializer):

    id = serializers.CharField()
    labels = serializers.ListField(child=serializers.CharField())
    properties = PropertiesField()


class RelationshipSerializer(serializers.Serializer):

    id = serializers.CharField()
    start = serializers.CharField()
    end = serializers.CharField()
    type = serializers.CharField()
    properties = PropertiesField()


class GraphResponseSerializer(serializers.Serializer):

    nodes = NodeSerializer(many=True)
    relationships = RelationshipSerializer(many=True, source="rels")
