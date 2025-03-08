from openai import OpenAI

# Initialize OpenAI client
client = OpenAI() 

# Create user profile with dietary preferences, cuisine type, and available ingredients
user_profile = {}
user_profile["dietary_restrictions"] = "no fat neither alcohol"
user_profile["cuisine_preferences"] = "boiled or raw food"
user_profile["ingredients_available"] = "eggs, water, flour, butter, salt, pepper, vegetables, pork"

# System prompt to instruct the AI on the task — generating an HTML recipe blog post
system_prompt  = {
  'role': 'system', 
  'content': 'Generate an enhanced HTML code for a recipe blog with inline CSS. Consider dietary restrictions, cuisine type, and ingredients.'
}

# User input for personalized recipe details
user_content1 = f"I want to create a recipe blog post. Here are my dietary restrictions: {user_profile['dietary_restrictions']}. My cuisine preferences include: {user_profile['cuisine_preferences']}. The ingredients I have available are: {user_profile['ingredients_available']}."

# Instructions for formatting the blog post
user_content2 = "Please provide a blog post with a title, description, ingredients, and instructions. Format the ingredients as a bulleted list and instructions as a numbered list. Include simple inline CSS for styling: use a clean font, soft colors, and space between sections."

# Constraint to use only the provided ingredients and limit the steps
user_content3 = "The recipe must use only the listed ingredients and should result in a single blog post with instructions not exceeding six steps. Ensure the HTML is clean and well-commented."

# Combine all user inputs into one request
user_prompt = {
  "role": "user",
  "content": user_content1 + "\n" + user_content2 + "\n" + user_content3
}

# Send the request to the OpenAI API to generate the HTML code
response = client.chat.completions.create(
  model="gpt-3.5-turbo", 
  messages=[system_prompt, user_prompt]
)

# Display the generated HTML content
print(response.choices[0].message.content)

