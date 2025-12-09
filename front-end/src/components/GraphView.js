// GraphView.jsx
import React, { useEffect, useState } from "react";
import { ForceGraph2D } from "react-force-graph";
import { useNavigate } from 'react-router-dom';

const GraphView = () => {
    const [data, setData] = useState({ nodes: [], links: [] });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // Load graph on mount
    useEffect(() => {
        const fetchGraph = async () => {
            try {
                const TOKEN = localStorage.getItem("access");
                setError(null);
                setLoading(true);

                const res = await fetch(`${process.env.REACT_APP_HTTP_HOST}/core/graph/`, {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${TOKEN}`,
                        "Content-Type": "application/json",
                    },
                });

                if (!res.ok) {
                    throw new Error(`Failed to load graph: ${res.status}`);
                }

                const json = await res.json();

                // Map nodes from Neo4j response
                const nodes = (json.nodes || []).map(n => ({
                    id: n.id,
                    label: n.properties?.name || (n.labels || []).join(","),
                    properties: n.properties || {},
                    labels: n.labels || [],
                }));

                // Map relationships (links)
                const links = (json.relationships || []).map(r => ({
                    source: r.start,
                    target: r.end,
                    label: r.type,
                    properties: r.properties || {},
                }));

                setData({ nodes, links });
            } catch (err) {
                console.error(err);
                setError("Could not load graph");
                // navigate("/login");
            } finally {
                setLoading(false);
            }
        };

        fetchGraph();
    }, []);

    const handleBackToChat = () => {
        navigate("/chat");
    }
    // Clear graph from server + UI
    const clearGraph = async () => {
        try {
            setError(null);
            const TOKEN = localStorage.getItem("access");
            const res = await fetch(`${process.env.REACT_APP_HTTP_HOST}/core/graph/`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${TOKEN}`,
                    "Content-Type": "application/json",
                },
            });

            if (!res.ok) {
                throw new Error(`Failed to delete graph: ${res.status}`);
            }

            setData({ nodes: [], links: [] });
        } catch (err) {
            console.error(err);
            setError("Could not clear graph");
        }
    };

    if (loading) return <p>Loading graph…</p>;

    return (
        <>
            <button
                onClick={clearGraph}
                disabled={data.nodes.length === 0}
                style={{ marginBottom: "10px" }}
            >
                Clear Graph
            </button>
            <button
                onClick={handleBackToChat}
                style={{ marginBottom: "10px" }}
            >
                Back To Chat
            </button>

            {error && (
                <p style={{ color: "red" }}>{error}</p>
            )}

            <div style={{ width: "100%", height: "90vh" }}>
                <ForceGraph2D
                    graphData={data}
                    nodeLabel={node => {
                        return (
                            node.label +
                            "\n" +
                            JSON.stringify(node.properties, null, 2)
                        );
                    }}
                    linkLabel={link => {
                        return (
                            link.label +
                            "\n" +
                            JSON.stringify(link.properties, null, 2)
                        );
                    }}
                    nodeAutoColorBy="labels"
                    linkDirectionalArrowLength={4}
                    linkDirectionalArrowRelPos={1}
                />
            </div>
        </>
    );
};

export default GraphView;
