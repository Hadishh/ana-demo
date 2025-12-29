import React, { useEffect, useState, useRef } from "react";
// Import Network from vis-network/standalone for the core visualization class
import { Network } from "vis-network/standalone";
import { useNavigate } from 'react-router-dom';

const GraphView = () => {
    // Reference to the DOM element for Vis.js to draw on
    const visJsRef = useRef(null);

    const [data, setData] = useState({ nodes: [], links: [] });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const TOKEN = localStorage.getItem("access");

    // --- Data Fetching Effect (Runs once on mount) ---
    useEffect(() => {
        const fetchGraph = async () => {
            try {
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

                // Map nodes from Django/Neo4j response to Vis.js format
                const nodes = (json.nodes || []).map(n => ({
                    id: n.id,
                    label: n.properties?.name || (n.labels || []).join(", "),
                    title: JSON.stringify(n.properties, null, 2),
                    group: n.labels[0] || 'default', // <--- Use the first label as the group key
                }));

                // Map relationships (edges)
                const links = (json.relationships || []).map(r => ({
                    from: r.start,
                    to: r.end,
                    label: r.properties?.name || r.type,
                    title: JSON.stringify(r.properties, null, 2),
                    arrows: 'to',
                }));

                setData({ nodes, links });
            } catch (err) {
                console.error(err);
                setError("Could not load graph");
            } finally {
                setLoading(false);
            }
        };

        fetchGraph();
    }, [TOKEN]); // FIX: Dependency array ensures this runs only on mount/token change

    // --- Vis.js Initialization Effect (Runs whenever data changes) ---
    useEffect(() => {
        if (visJsRef.current && data.nodes.length > 0) {
            const visData = {
                nodes: data.nodes,
                edges: data.links, // Vis.js uses 'edges'
            };

            const options = {
                layout: {
                    // This is crucial for a stable, repeatable layout
                    improvedLayout: true
                },
                groups: {
                    'Episodic': {
                        color: { background: '#32CD32', border: '#228B22' }, // Neon Green
                        shape: 'dot',
                        size: 30,
                        font: { color: '#FFFFFF' }
                    },
                    'Entity': {
                        color: { background: '#1E90FF', border: '#4682B4' }, // Dodger Blue
                        shape: 'dot',
                        size: 30,
                        font: { color: '#FFFFFF' }
                    },
                    // Add a default group for nodes with no labels
                    'default': {
                        color: { background: '#808080', border: '#696969' },
                        shape: 'dot',
                        size: 20,
                        font: { color: '#FFFFFF' }
                    },
                },

                nodes: {
                    borderWidth: 2,
                    // Default font settings for nodes
                    font: {
                        size: 14,
                        color: '#FFFFFF', // White text on dark background
                        face: 'Arial',
                        align: 'center'
                    },
                    shadow: { // Add a slight glow/shadow
                        enabled: true,
                        color: 'rgba(255, 255, 255, 0.5)',
                        size: 10,
                        x: 0,
                        y: 0
                    }
                },
                edges: {
                    color: { inherit: 'from', highlight: '#FFD700' }, // Gold highlight on hover
                    width: 2,
                    arrows: { to: { enabled: true, scaleFactor: 0.5 } },
                    smooth: { type: 'continuous' },
                    font: {
                        size: 8, // Smaller font for less clutter
                        color: '#ffffffff', // Light green color for links
                        face: 'Arial',
                        align: 'middle',
                        weight: 'normal',
                        strokeWidth: 0,
                        vadjust: -1,
                    }
                },
                // FIX: Correct physics configuration for stabilization
                physics: {
                    enabled: true,
                    barnesHut: {
                        gravitationalConstant: -5000, // Increased gravity for slightly tighter clustering
                        springConstant: 0.05,
                        springLength: 150,
                        damping: 0.09
                    },
                    stabilization: {
                        enabled: true,
                        iterations: 1500, // Slightly more iterations for stability
                    }
                },

                interaction: {
                    hover: true,
                    tooltipDelay: 200,
                }
                // The error-causing 'configure' block has been removed.
            };

            const network = new Network(visJsRef.current, visData, options);

            // OPTIONAL: Stop physics after stabilization for a static final view
            network.once('stabilized', function () {
                network.setOptions({ physics: false });
            });


            // Cleanup function
            return () => {
                if (network) {
                    network.destroy();
                }
            };
        }
    }, [data]); // Re-run when graph data changes (load or clear)


    // --- Handlers ---
    const handleBackToChat = () => {
        navigate("/chat");
    }

    const clearGraph = async () => {
        try {
            setError(null);

            const res = await fetch(`${process.env.REACT_APP_HTTP_HOST}/core/graph/`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${TOKEN}`, "Content-Type": "application/json" },
            });

            if (!res.ok) {
                throw new Error(`Failed to delete graph: ${res.status}`);
            }

            // Clear the data state to trigger useEffect and refresh the graph
            setData({ nodes: [], links: [] });
        } catch (err) {
            console.error(err);
            setError("Could not clear graph");
        }
    };

    if (loading) return <p>Loading graph…</p>;

    return (
        <>
            <div style={{ padding: "10px", display: "flex", gap: "10px" }}>
                <button
                    onClick={clearGraph}
                    disabled={data.nodes.length === 0}
                >
                    Clear Graph
                </button>
                <button
                    onClick={handleBackToChat}
                >
                    Back To Chat
                </button>
            </div>

            {error && (
                <p style={{ color: "red", padding: "0 10px" }}>{error}</p>
            )}

            {/* The container element for the Vis.js visualization */}
            <div
                ref={visJsRef}
                style={{ width: "100%", height: "90vh", backgroundColor: "#333", border: "1px solid #000" }}
            />
        </>
    );
};

export default GraphView;