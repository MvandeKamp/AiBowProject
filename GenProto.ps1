python -m grpc_tools.protoc --proto_path=.\AiBowProject.API --python_out=.\Orchestrator\src\proto --grpc_python_out=.\Orchestrator\src\proto aiClientDef.proto
python -m grpc_tools.protoc --proto_path=.\AiBowProject.API --python_out=.\Orchestrator\src\proto --grpc_python_out=.\Orchestrator\src\proto greeting.proto
