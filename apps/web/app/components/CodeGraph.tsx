"use client";

import {

    Background,

    Controls,

    MiniMap,

    ReactFlow,

    Node,

    Edge,

} from "reactflow";

import "reactflow/dist/style.css";

import dagre from "@dagrejs/dagre";

import { Trace } from "../types/chat";

import { useState } from "react";

type Props={

    trace?:Trace;

};

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

    if(!trace) return null;

    const [selectedNode, setSelectedNode] = useState<any>(null);

    const nodes: Node[] = trace.graph_nodes.map((node) => ({

        id: node.id,

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

                    fitView

                    onNodeClick={(_, node) => {

                        setSelectedNode(node.data);

                    }}

                >

                    <MiniMap/>

                    <Controls/>

                    <Background/>

                </ReactFlow>

            </div>

            {

                        selectedNode && (

                        <div
                        className="mt-6 rounded-xl border border-zinc-700 bg-zinc-900 p-5"
                        >

                        <h3 className="text-xl font-bold">

                        {selectedNode.label}

                        </h3>

                        <div className="mt-4 space-y-2 text-sm">

                        <div>

                        <b>Type:</b> {selectedNode.type}

                        </div>

                        <div>

                        <b>File:</b> {selectedNode.file_path}

                        </div>

                        <div>

                        <b>Lines:</b>

                        {" "}

                        {selectedNode.start_line}

                        -

                        {selectedNode.end_line}

                        </div>

                        <div>

                        <b>Description:</b>

                        </div>

                        <p className="text-zinc-400">

                        {selectedNode.description}

                        </p>

                        </div>

                        </div>

                        )

                    }

        </div>

    );

}