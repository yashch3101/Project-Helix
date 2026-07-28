"use client";

import {
    Background,
    Controls,
    MiniMap,
    ReactFlow,
    Node,
    Edge,
    Handle,
    Position,
} from "reactflow";

import { FileCode2 } from "lucide-react";

import "reactflow/dist/style.css";

import dagre from "@dagrejs/dagre";

import { ReasoningTrace } from "../types/chat";

import { useMemo, useState } from "react";

type Props={

    trace?:ReasoningTrace;

};

function GraphNode({
    data,
}: {
    data: ReasoningTrace["graph_nodes"][number];
}) {
    return (
        <div className="min-w-[220px] rounded-xl border border-violet-500/20 bg-zinc-900/90 backdrop-blur-md shadow-lg hover:border-violet-500/40 transition-all">

            <Handle
                type="target"
                position={Position.Top}
            />

            <div className="flex items-center gap-3 p-4">

                <div className="rounded-lg bg-violet-500/10 p-2">

                    <FileCode2
                        size={18}
                        className="text-violet-300"
                    />

                </div>

                <div className="overflow-hidden">

                    <p className="truncate text-sm font-semibold text-white">

                        {data.label}

                    </p>

                    <p className="truncate text-xs text-zinc-400">

                        {data.type || "Repository Symbol"}

                    </p>

                </div>

            </div>

            <Handle
                type="source"
                position={Position.Bottom}
            />

        </div>
    );
}

const dagreGraph = new dagre.graphlib.Graph();

dagreGraph.setDefaultEdgeLabel(() => ({}));

const nodeWidth = 220;
const nodeHeight = 60;

function getLayoutedElements(nodes: Node[], edges: Edge[]) {

    dagreGraph.setGraph({

        rankdir: "TB",

        nodesep: 60,

        ranksep: 120,

    });

    nodes.forEach((node) => {

        dagreGraph.setNode(node.id, {

            width: nodeWidth,

            height: nodeHeight,

        });

    });

    edges.forEach((edge) => {

        dagreGraph.setEdge(

            edge.source,

            edge.target

        );

    });

    dagre.layout(dagreGraph);

    nodes.forEach((node) => {

        const position = dagreGraph.node(node.id);

        node.position = {

            x: position.x - nodeWidth / 2,

            y: position.y - nodeHeight / 2,

        };

    });

    return {

        nodes,

        edges,

    };

}

export default function CodeGraph({

    trace,

}:Props){

const [selectedNode, setSelectedNode] =
    useState<ReasoningTrace["graph_nodes"][number] | null>(null);

        const nodeTypes = useMemo(
            () => ({
                custom: GraphNode,
            }),
            []
        );

        if (!trace) return null;

    const nodes: Node[] = trace.graph_nodes.map((node) => ({

        id: node.id,
        type: "custom",
        data: {

            ...node,

            label: node.label,

        },

        position: {

            x: 0,

            y: 0,

        },

    }));

    const edges:Edge[] = trace.graph_connections.map(

        (edge,index)=>({

            id:String(index),

            source:edge.source,

            target:edge.target,

            animated:true,

            label:edge.relation,

        })

    );

    const layout = getLayoutedElements(

        nodes,

        edges

    );

    return(

        <div className="mt-6">

            <h3 className="font-semibold text-lg mb-4">

                🕸 Repository Call Graph

            </h3>

            <div className="h-[600px] rounded-xl overflow-hidden border border-zinc-800">

                <ReactFlow
                    nodes={layout.nodes}
                    edges={layout.edges}
                    nodeTypes={nodeTypes}
                    proOptions={{ hideAttribution: true }}
                    defaultEdgeOptions={{
                        style: {
                            stroke: "#7c3aed",
                            strokeWidth: 2,
                        },
                    }}
                    fitView

                    onNodeClick={(_, node) => {

                        setSelectedNode(node.data);

                    }}

                >

                    <MiniMap
                        pannable
                        zoomable
                        className="bg-zinc-900"
                    />

                    <Controls/>

                    <Background gap={24} size={1} color="#3f3f46" />

                </ReactFlow>

            </div>

            {

                        selectedNode && (

                        <div
                        className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900/70 backdrop-blur-md p-6"
                        >

                        <h3 className="text-xl font-bold">

                        {selectedNode.label}

                        </h3>

                        <div className="mt-4 space-y-2 text-sm">

                        <div className="mt-1 inline-flex rounded-full border border-violet-500/20 bg-violet-500/10 px-2 py-1 text-xs text-violet-300">

                        <b>Type:</b> {selectedNode.type}

                        </div>

                        <div>

                        <b>File:</b> {selectedNode.file_path || "Unknown"}

                        </div>

                        <div>

                        <b>Lines:</b>

                        {" "}

                        {selectedNode.start_line ?? "-"}
                        {" - "}
                        {selectedNode.end_line ?? "-"}

                        </div>

                        <div>

                        <b>Description:</b>

                        </div>

                        <p className="text-zinc-400">
                            {selectedNode.description || "No description available."}
                        </p>

                        </div>

                        </div>

                        )

                    }

        </div>

    );

}