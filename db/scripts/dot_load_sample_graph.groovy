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
    ctx.logger.info("==> Starting up... Loading graph from GraphSON file")

    //Kyro:
    //graph.io(GryoIo.build()).readGraph('data/dot_graph.kryo')

    //GraphML:
    graph.io(IoCore.graphml()).readGraph('data/dot_graph.graphml')
    //GraphSON
    //graph.io(IoCore.graphson()).readGraph('data/dot_graph.graphson')


    ctx.logger.info("==> Graph data loaded")
  },
  onShutDown: { ctx ->
    ctx.logger.info("Shutting Down... Saving graph to GraphML file")
    graph.io(graphml()).writeGraph('data/dot_graph.graphml')

    ctx.logger.info("Shutting Down... Saving graph to GraphSON file")
    graph.io(IoCore.graphson()).writeGraph('data/dot_graph.graphson')

    ctx.logger.info("Shutting Down... Saving graph to kryo file")
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
