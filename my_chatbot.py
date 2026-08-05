import streamlit as st
import groq

client = groq.Groq(api_key=st.secrets["GROQ_KEY"])

st.title("Gadget Shop AI")

knowledge_base = [
  "Free delivery for orders above P10,000. Standard delivery takes 2-4 days.",
  "We are open from 9:00 AM to 9:00 PM daily, Monday to Sunday.",
  "We accept cash, credit card, GCash, and Maya payments.",
  "All products have a 1-year official warranty.",
  "Our return policy allows return within 7 days if the product is unopened",
  "The iPhone 15 is priced at 45,000 pesos with A16 Bionic chip.",
  "The Samsung Galaxy S24 is priced at 55,000 pesos with snapdragon 8 Gen 3.",
  "The Airpods Pro costs 12,000 pesos with noise cancellation.",
  "Order processing takes 24hours before shipping.",
  "We have a physical store in SM Mall of Asia, Metro Manila."
  "The owner of the Shop is Anzar Pogi"
]

def retrieve(q):
  scored = []
  for i, doc in enumerate(knowledge_base):
    score = 0
    for word in q.split():
      if word in doc.lower():
        score += 1
    scored.append((score, i, doc))
  scored.sort(reverse=True)
  best = scored[0]
  return best

def build_context(q):
  context = []
  for doc in knowledge_base:
    matches = sum(1 for word in q.split() if word in doc.lower())
    if matches > 0:
      context.append(doc)
  return ";".join(context[:3])

products = [
  {"name": "iPhone 15", "price": 45000, "stock": 10},
  {"name": "Samsung Galaxy S24", "price": 55000, "stock": 5},
  {"name": "Google Pixel 8", "price": 35000, "stock": 8},
  {"name": "Airpods Pro", "price": 12000, "stock": 15},
  {"name": "iPad Air", "price": 35000, "stock": 7},
]

def find_product(q):

  for p in products:
    if p["name"].lower() in q:
      return p
  
  return None

if "messages" not in st.session_state:
  st.session_state.messages = [
    {"role": "assistant", "content": "Hello! I'm Gadget Shop AI. Ask me about products, prices, stock, delivery, or payment."}
  ]

for msg in st.session_state.messages:
  with st.chat_message(msg["role"]):
    st.write(msg["content"])

# Chat input 
question = st.chat_input("Ask me anything...")

# Kapag may tinype ang user 
if question: 

  st.session_state.messages.append({"role": "user", "content": question})
  
  q = question.lower()

  try:
    context = build_context(q)

    system_prompt = (
      "You are Gadget Shop AI, a helpful assistant for a gadget shop in the Philippines. "
      "Answer in Taglish if the user asks in Taglish, otherwise answer in English. "
      "Be friendly, concise, and helpful.\n\n"
      f"Knowledge base (use as reference if relevant): {context}"
    )

    response = client.chat.completions.create(
      model="llama-3.3-70b-versatile",
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Customer question: {question}"}
      ]
    )
    answer = response.choices[0].message.content

  except Exception as e:
    answer = f"Sorry, may problema sa AI connection: {e}"

  st.session_state.messages.append({"role": "assistant", "content": answer})

  # Ipakita sa screen 
  with st.chat_message("user"):
    st.write(question)
  with st.chat_message("assistant"):
    st.write(answer)