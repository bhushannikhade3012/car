def apnabot(prompt, chat_history=[]):
    import google.generativeai as genai

    genai.configure(api_key="AIzaSyDb7OmnXTrpb2dUbS8CFne9H_cfxdgAmAM")
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Add the current user input to the history
    chat_history.append(f"User: {prompt}")
    
    # Combine the chat history into a single prompt
    context = "\n".join(chat_history) + "\nBot:"
    
    # Get the model's response
    response = model.generate_content(context)
    
    # Append the bot's response to the chat history
    chat_history.append(f"Bot: {response.text.strip()}")
    
    return response.text.strip(), chat_history
