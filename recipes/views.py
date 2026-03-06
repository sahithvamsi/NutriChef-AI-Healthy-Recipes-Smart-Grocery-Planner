import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Recipe, MealPlan

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from groq import Groq


# ==========================================
# RECIPE GENERATOR
# ==========================================
@login_required
def recipe_generator_view(request):

    recipe = None

    # 🔹 If user clicks a saved recipe
    recipe_id = request.GET.get("recipe_id")
    if recipe_id:
        saved_recipe = get_object_or_404(
            Recipe,
            id=recipe_id,
            user=request.user
        )

        try:
            recipe = json.loads(saved_recipe.generated_recipe)
        except json.JSONDecodeError:
            recipe = {"error": "Saved recipe data is corrupted."}

    # 🔹 If generating new recipe
    if request.method == "POST":

        ingredients = request.POST.get("ingredients")
        meal_type = request.POST.get("type")
        goal = request.POST.get("goal")
        cuisine = request.POST.get("cuisine")
        time = request.POST.get("time")
        spice = request.POST.get("spice")
        budget = request.POST.get("budget")

        try:
            llm = ChatGroq(
                groq_api_key=settings.GROQ_API_KEY,
                model_name=settings.GROQ_MODEL,
                temperature=0.7
            )

            prompt = ChatPromptTemplate.from_template("""
You are a certified professional chef and nutrition expert and you must strictly follow all user selections without exception. If the selected dietary category conflicts with the provided ingredients (for example chicken selected while Vegetarian or Vegan is chosen), you must immediately return an error and not generate a recipe. If the provided budget or time is insufficient to realistically prepare the requested dish, you must return an appropriate error instead of adjusting values unrealistically. You must generate a recipe using only the ingredients explicitly provided by the user and you are strictly forbidden from adding extra ingredients such as water, salt, oil, spices, or any other common items unless they are clearly mentioned in the input. Always respond in strict valid JSON only with no explanations, no markdown, and no extra text

Create a detailed {meal_type} recipe using {ingredients}.
Goal: {goal}
Cuisine: {cuisine}
Cooking Time: {time}
Spice Level: {spice}
Budget: {budget}

Preparation steps must be VERY detailed and beginner friendly.
Each step must explain heat level, cooking method, timing, and texture changes.

Respond ONLY in valid JSON.
Do NOT add explanation.
Do NOT add markdown.

Return format:

{{
    "recipe_name": "",
    "ingredients": [
        {{
            "item": "",
            "quantity": "",
            "calories": "",
            "protein": "",
            "carbs": "",
            "fat": "",
            "cost": ""
        }}
    ],
    "steps": [
        "Step 1: ...",
        "Step 2: ..."
    ]
}}
""")

            chain = prompt | llm

            response = chain.invoke({
                "meal_type": meal_type,
                "ingredients": ingredients,
                "goal": goal,
                "cuisine": cuisine,
                "time": time,
                "spice": spice,
                "budget": budget
            })

            output_text = response.content.strip()

            # Remove markdown if model adds ```
            if output_text.startswith("```"):
                parts = output_text.split("```")
                if len(parts) > 1:
                    output_text = parts[1].strip()

            try:
                recipe_data = json.loads(output_text)
                recipe = recipe_data

                # Save in database
                Recipe.objects.create(
                    user=request.user,
                    title=recipe_data.get("recipe_name", "AI Recipe"),
                    ingredients=ingredients,
                    generated_recipe=json.dumps(recipe_data)  # store clean JSON
                )

            except json.JSONDecodeError:
                recipe = {"error": "AI returned invalid JSON. Please try again."}

        except Exception as e:
            recipe = {"error": str(e)}

    # 🔹 Send saved recipes to generator page
    my_recipes = Recipe.objects.filter(
        user=request.user
    ).order_by("-created_at")[:10]

    return render(request, "recipes/generator.html", {
        "recipe": recipe,
        "my_recipes": my_recipes
    })


# ==========================================
# MY RECIPES PAGE
# ==========================================
@login_required
def my_recipes(request):

    recipes = Recipe.objects.filter(
        user=request.user
    ).order_by("-created_at")

    for r in recipes:
        try:
            r.parsed_recipe = json.loads(r.generated_recipe)
        except:
            r.parsed_recipe = None

    return render(request, "recipes/my_recipes.html", {
        "recipes": recipes
    })




# =====================================
# SHOPPING LIST
# =====================================
@login_required
def shopping_list_view(request):

    recipe = None

    if request.method == "POST":

        budget = request.POST.get("budget")
        food_type = request.POST.get("food_type")
        goal = request.POST.get("goal")
        cuisine = request.POST.get("cuisine")

        prompt = f"""
Create a {food_type} recipe under budget {budget}.
Goal: {goal}
Cuisine: {cuisine}

Provide:
1. Recipe name
2. Ingredients with approximate cost
3. Step-by-step instructions
4. Total estimated cost
"""

        client = Groq(api_key=settings.GROQ_API_KEY)

        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        recipe = response.choices[0].message.content

    return render(request, "recipes/shopping_list.html", {
        "recipe": recipe
    })


# ==========================================
# DELETE RECIPE
# ==========================================
@login_required
def delete_recipe(request, pk):

    recipe = get_object_or_404(
        Recipe,
        id=pk,
        user=request.user
    )

    recipe.delete()

    # Redirect back safely
    return redirect(request.META.get('HTTP_REFERER', 'saved_recipes'))

@login_required
def health_supporter_view(request):

    health_result = None

    if request.method == "POST":

        problem = request.POST.get("problem")

        try:
            llm = ChatGroq(
                groq_api_key=settings.GROQ_API_KEY,
                model_name=settings.GROQ_MODEL,
                temperature=0.5
            )

            prompt = ChatPromptTemplate.from_template("""
You are a professional nutritionist and health recovery expert.

A person is facing this health issue:
{problem}

Based on the severity of the problem:

- If it is mild (like gas, indigestion, mild cold), give a 1-day or 2-day recovery plan.
- If it is moderate (fever, weakness, infection recovery), give a 3–7 day structured recovery plan.
- Keep it simple, practical, and safe.

Provide a structured day-wise food plan.

Respond ONLY in valid JSON.
Do NOT add explanation.
Do NOT add markdown.

Return format:

{{
    "problem": "",
    "duration": "1 Day / 3 Days / 7 Days",
    "plan": [
        {{
            "day": "Day 1",
            "morning": "",
            "breakfast": "",
            "lunch": "",
            "evening": "",
            "dinner": ""
        }}
    ],
    "general_do": "",
    "avoid": "",
    "important_note": "This is general advice. Consult a doctor if symptoms are severe or persistent."
}}
""")

            chain = prompt | llm

            response = chain.invoke({
                "problem": problem
            })

            output_text = response.content.strip()

            # Remove markdown if model adds ```
            if output_text.startswith("```"):
                parts = output_text.split("```")
                if len(parts) > 1:
                    output_text = parts[1].strip()

            try:
                health_data = json.loads(output_text)
                health_result = health_data

            except json.JSONDecodeError:
                health_result = {
                    "error": "AI returned invalid JSON. Please try again."
                }

        except Exception as e:
            health_result = {
                "error": str(e)
            }

    return render(request, "recipes/health_supporter.html", {
        "health_result": health_result
    })