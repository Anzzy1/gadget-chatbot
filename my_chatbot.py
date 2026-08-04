import streamlit as st

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
  
  # Simple response logic 
  q = question.lower()

  if "hello" in q or "hi" in q:
    intent = "greeting"
  elif "price" in q or "magkano" in q or "how much" in q or "cost" in q:
    intent = "price"
  elif "stock" in q or "available" in q or "available pa" in q:
    intent = "stock"
  elif "hours" in q or "open" in q or "oras" in q or "bukas"in q:
    intent = "hours"
  elif "thank" in q or "salamat" in q:
    intent = "thanks"
  else:
    intent = "unknown"

  product = find_product(q)

  if intent == "greeting":
    answer = "Hello! Ask me about products."
  elif intent == "price":
    if product:
      answer = f"The product {product['name']} costs P{product['price']:,} pesos."
    else:
      answer = "Whic product? Try asking 'price of iPhone 15'"
  elif intent == "stock":
    if product:
      answer = f"We have {product['stock']} units of {product['name']} in stock."
    else:
      answer = "Whic product? Try asking 'Do you have stock of Airpods'"
  elif intent == "hours":
    answer = "We are open from 9:00 AM to 9:00 PM daily."
  elif intent == "thanks":
    answer = "You're welcome!"
  else:
    score, index, best_doc = retrieve(q)
    if score > 0:
      answer = f"I found relevant info: {best_doc}"
    else:
      answer = "Sorry, I don't have an answer for that yet."

  st.session_state.messages.append({"role": "assistant", "content": answer})

  # Ipakita sa screen 
  with st.chat_message("user"):
    st.write(question)
  with st.chat_message("assistant"):
    st.write(answer)