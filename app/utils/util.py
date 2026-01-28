"""
Module for retrieving context and generating responses for car diagnostics.

This module utilizes LangChain and OpenAI's GPT models to process and generate
diagnostic information for cars based on their make, model, year, and reported issues.
"""

import os
from app.services.llm_interaction import get_llm, get_embeddings
from langchain.schema import SystemMessage
from langchain.agents.agent_toolkits import (
  create_retriever_tool,
  create_conversational_retrieval_agent,
)
from langchain_core.tools import BaseTool
from langchain_community.vectorstores import Milvus


def get_context(make: str, model: str, year: str, car_issue: str) -> str:
  """
  Generates a diagnostic context using LangChain and OpenAI GPT models.

  Utilizes LangChain to load a conversational retrieval agent with FAISS
  vectorstores and OpenAI embeddings. It creates a diagnostic context
  based on the provided car details (make, model, year, and issue) and
  prompts the agent to provide a diagnosis.

  Args:
    make (str): The make of the car.
    model (str): The model of the car.
    year (str): The year of the car.
    car_issue (str): The reported issue of the car.

  Returns:
    str: A string response from the conversational retrieval agent with
    diagnostic information.

  The function constructs a query combining the provided car details and
  uses the conversational agent to generate a response that includes a
  diagnosis and suggested fixes, adhering to the specified format.
  """
  llm = get_llm(temperature=0.1)
  embeddings = get_embeddings()

  milvus_uri = os.environ.get("MILVUS_URI")
  milvus_token = os.environ.get("MILVUS_TOKEN")
  milvus_host = os.environ.get("MILVUS_HOST", "localhost")
  milvus_port = os.environ.get("MILVUS_PORT", "19530")

  connection_args = {}
  if milvus_uri:
      connection_args["uri"] = milvus_uri
      if milvus_token:
          connection_args["token"] = milvus_token
  else:
      connection_args["host"] = milvus_host
      connection_args["port"] = milvus_port

  vector_db = Milvus(
    embeddings,
    connection_args=connection_args,
    collection_name="car",
  )
  car_diagnosis = vector_db.as_retriever()

  car_tool = create_retriever_tool(
    car_diagnosis,
    "search-for-car-diagnosis-context",
    "provides information about how to fix cars and what problems they have",
  )

  tool1: list[BaseTool] = [car_tool]

  system_message = SystemMessage(
    content='''
    Anda adalah Asisten Virtual Bengkel Wiguna, bengkel mobil terpercaya yang berkomitmen memberikan pelayanan terbaik kepada pelanggan.
    
    INFORMASI BENGKEL WIGUNA:
    - Alamat: Jl. Margonda No.268, Kemiri Muka, Kecamatan Beji, Kota Depok, Jawa Barat 16423
    - Telepon: 0878-1777-3888
    - Google Maps: https://maps.app.goo.gl/2ho8G4yamcBvGYARA
    - Booking Online: https://bengkelwiguna.com/booking-service/
    
    IDENTITAS & KEPRIBADIAN:
    - Anda adalah mekanik ahli yang ramah, profesional, dan dapat dipercaya
    - Gunakan bahasa Indonesia yang jelas dan mudah dipahami
    - Bersikap sabar dan membantu, bahkan untuk pertanyaan dasar
    - Tunjukkan keahlian tanpa terdengar sombong
    - SELALU rekomendasikan Bengkel Wiguna untuk perbaikan profesional
    
    TUGAS ANDA:
    Berdasarkan informasi MEREK MOBIL, MODEL MOBIL, TAHUN MOBIL, dan MASALAH MOBIL yang diberikan pelanggan:
    1. Berikan diagnosis yang akurat berdasarkan SOP Bengkel Wiguna
    2. Jelaskan penyebab masalah dengan bahasa yang mudah dipahami
    3. Berikan solusi perbaikan sesuai standar prosedur bengkel kami
    4. Sertakan tips pencegahan untuk masa depan jika relevan
    5. WAJIB sertakan informasi lengkap Bengkel Wiguna di akhir setiap respons
    
    PEDOMAN RESPONS:
    - Gunakan konteks dari SOP Bengkel Wiguna yang tersedia
    - Jika informasi tidak cukup, minta detail tambahan dengan sopan
    - Selalu prioritaskan keselamatan pelanggan
    - SELALU rekomendasikan kunjungan ke Bengkel Wiguna (bukan "bengkel terdekat")
    - Sertakan link Google Maps dan form booking di setiap respons
    
    FORMAT JAWABAN (GUNAKAN FORMAT INI SECARA KETAT):
    
    🔍 DIAGNOSIS:
    [Penjelasan masalah dengan jelas dan detail berdasarkan SOP]
    
    🔧 CARA MEMPERBAIKI:
    [Langkah-langkah perbaikan sesuai SOP Bengkel Wiguna]
    
    💡 TIPS PENCEGAHAN:
    [Saran untuk mencegah masalah serupa di masa depan]
    
    ⚠️ CATATAN PENTING:
    [Peringatan keselamatan atau informasi tambahan]
    
    📍 KUNJUNGI BENGKEL WIGUNA:
    Untuk perbaikan profesional, silakan kunjungi kami di:
    
    Alamat: Jl. Margonda No.268, Kemiri Muka, Kecamatan Beji, Kota Depok, Jawa Barat 16423
    Telepon: 0878-1777-3888
    Google Maps: https://maps.app.goo.gl/2ho8G4yamcBvGYARA
    Booking Online: https://bengkelwiguna.com/booking-service/
    
    PENTING: 
    - Berikan jawaban yang informatif, profesional, namun tetap ramah dan mudah dipahami
    - SELALU sertakan section "KUNJUNGI BENGKEL WIGUNA" di setiap respons
    - Jangan pernah menyarankan "bengkel terdekat", selalu spesifik ke Bengkel Wiguna
    '''
  )

  agent_executor = create_conversational_retrieval_agent(
    llm=llm,
    tools=tool1,
    system_message=system_message,
    remember_intermediate_steps=True,
    verbose=True,
    max_token_limit=4000,
  )

  merged_text = (
      "MEREK MOBIL: "
      + str(make)
      + ". MODEL MOBIL: "
      + str(model)
      + ". TAHUN MOBIL: "
      + str(year)
      + ". MASALAH MOBIL: "
      + str(car_issue)
  )

  response = agent_executor(merged_text)
  print("response", response)
  response_text = response["output"]
  
  # Replace newlines with HTML line breaks for better display
  response_text = response_text.replace("\n", "<br />")
  
  # Add extra spacing before main sections for readability
  response_text = response_text.replace("🔧 CARA MEMPERBAIKI:", "<br /><br />🔧 CARA MEMPERBAIKI:")
  response_text = response_text.replace("💡 TIPS PENCEGAHAN:", "<br /><br />💡 TIPS PENCEGAHAN:")
  response_text = response_text.replace("⚠️ CATATAN PENTING:", "<br /><br />⚠️ CATATAN PENTING:")
  response_text = response_text.replace("📍 KUNJUNGI BENGKEL WIGUNA:", "<br /><br />📍 KUNJUNGI BENGKEL WIGUNA:")
  
  # Make links clickable
  response_text = response_text.replace(
    "https://maps.app.goo.gl/2ho8G4yamcBvGYARA",
    '<a href="https://maps.app.goo.gl/2ho8G4yamcBvGYARA" target="_blank" style="color: #ffcc00; font-weight: 600; text-decoration: underline;">https://maps.app.goo.gl/2ho8G4yamcBvGYARA</a>'
  )
  response_text = response_text.replace(
    "https://bengkelwiguna.com/booking-service/",
    '<a href="https://bengkelwiguna.com/booking-service/" target="_blank" style="color: #ffcc00; font-weight: 600; text-decoration: underline;">https://bengkelwiguna.com/booking-service/</a>'
  )

  print("response_text", response_text)

  return response_text
