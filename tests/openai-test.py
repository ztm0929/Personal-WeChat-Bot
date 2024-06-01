from openai import OpenAI
import json

client = OpenAI()

def get_current_weather(location, unit="℃"):
    if "shenzhen" in location.lower():
        return json.dumps({"location": "Shenzhen", "temperature": 30, "unit": unit})
    elif "guangzhou" in location.lower():
        return json.dumps({"location": "Guangzhou", "temperature": 32, "unit": unit})
    elif "beijing" in location.lower():
        return json.dumps({"location": "Beijing", "temperature": 25, "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

def run_conversation():
    messages = [{"role": "user", "content": "What's the weather in Shenzhen, Guangzhou, and beiJing?"}]
    tools = [{
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather of a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to get the weather"
                    },
                    "unit": {
                        "type": "string",
                        "description": "The unit of the temperature"
                    }
                },
                "required": ["location"]
            }
        }
    }]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "get_current_weather": get_current_weather
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit")
            )
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            })
        second_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        return second_response
print(run_conversation())