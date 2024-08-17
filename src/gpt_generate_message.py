def generate_message(client, ceo_name, email, company_name, company_description, user_name):
    # Construct the ChatGPT prompt
    prompt = (f"""CEO's Name: {ceo_name} 
        CEO's Company name: {company_name} 
        This is information about the CEO's company: {company_description}
        Email Template:

        Dear [CEO's Name],

        
        # You can put your actual content here.

        
        Warm regards,

        {user_name}
    """)

    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )

    # Extract and print the assistant's response
    response_message = chat_completion.choices[0].message
    return response_message.content