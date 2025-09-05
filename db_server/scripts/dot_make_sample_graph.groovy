/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

// Functions defined here will go into global cache and
// will not be removed from there unless there is a reset
// of the ScriptEngine.
def addItUp(x, y) { x + y }

// an init script that returns a Map allows
// explicit setting of global bindings.
def globals = [:]

// Defines a sample LifeCycleHook that prints some output
// to the Gremlin Server console. Note that the name of
// the key in the "global" map is unimportant.
globals << [hook : [
  onStartUp: { ctx ->
    ctx.logger.warn("==> Adding custom vertices to empty graph using 'graph.addVertex(...)':")

    graph.addVertex(
      T.label, "issue",
      "date", "",
      "name", "Facility Capacity is 20.000 boe/day",
      "index", "",
      "description", "",
      "tag", "facility",
      "type", "fact",
      "uuid", "8f6c80c6-cf72-4de0-8dbe-a122b17a9a4b",
      "shortname", "",
      "timestamp", ""
      )
    graph.addVertex(
      T.label, "issue",
      "date", "",
      "name", "Drilling Time is uncertain. But most likely 60 days. In the worst case, side track needs to be drilled which adds around 20 days.",
      "index", "",
      "description", "",
      "tag", "drilling",
      "type", "uncertainty",
      "uuid", "0b6bcc29-4308-44f2-8052-9f81dba81c8e",
      "shortname", "",
      "timestamp", ""
      )
    graph.addVertex(
      T.label, "issue",
      "date", "",
      "name", "Production Performance is uncertain based on the reservoir simulations. P10, P90 and mean production can be provided.",
      "index", "",
      "description", "",
      "tag", "subsurface",
      "type", "uncertainty",
      "uuid", "abfab7a2-cf55-40b8-8883-8e9edefe51c6",
      "shortname", "",
      "timestamp", ""
      )
    graph.addVertex(
      T.label, "issue",
      "date", "",
      "name", "Maximize NPV",
      "index", "",
      "description", "",
      "tag", "financial",
      "type", "decision metric",
      "uuid", "5f622a1c-8473-4769-8e50-e81ea7dbb474",
      "shortname", "",
      "timestamp", ""
      )

    ctx.logger.warn("==> Graph data file created in 'data' folder")

    //Kyro:
    //graph.io(GryoIo.build()).readGraph('data/sample.kryo')
    //GraphML:
    //graph.io(IoCore.graphml()).readGraph('dot_graph.graphml')

    //hook on shutDown: save graph as GraphML file
    //graph.io(graphml()).writeGraph('dot_graph.graphml')

  },
  onShutDown: { ctx ->
    ctx.logger.warn("==> Shutting Down... Saving graph to GraphML file")
    graph.io(graphml()).writeGraph('data/dot_graph.graphml')

    ctx.logger.warn("==> Shutting Down... Saving graph to kryo file")
    graph.io(GryoIo.build()).writeGraph('data/dot_graph.kryo')
  }
] as LifeCycleHook]

// define the default TraversalSource to bind queries to -
// this one will be named "g".

// ReferenceElementStrategy converts all graph elements
// (vertices/edges/vertex properties) to "references"
// (i.e. just id and label without properties).

// This strategy was added in 3.4.0 to make all Gremlin
// Server results consistent across all protocols and
// serialization formats aligning it with TinkerPop
// recommended practices for writing Gremlin.
globals << [g : traversal().withEmbedded(graph).withStrategies(ReferenceElementStrategy)]
