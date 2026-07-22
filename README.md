# 🏫 Cambridge Automision — AI-Powered Smart School Management & Parent Communication System

> **Final Project Submission — Ship Your AI App**  
> **Course:** AI Application Development  
> **Developer:** Khursheed Ahmed  
> **Live App URL:** [https://cambridge-automision.streamlit.app/](https://cambridge-automision.streamlit.app/)

---

## 📌 Problem Statement & Core Idea

### The Problem:
Managing daily school operations—such as attendance tracking, parent communication, and daily diary distribution—is highly time-consuming for teachers. Traditional channels like printed diaries or manual WhatsApp broadcasting lead to miscommunication, forgotten home tasks, and delayed absence notifications to parents.

### The Solution:
**Cambridge Automision** is a lightweight, cloud-based school management platform integrated with **Google Sheets** and powered by **Google Gemini AI**. It bridges the communication gap between school staff and parents by automating attendance tracking, enabling 1-click direct WhatsApp absence alerts, and leveraging AI to convert raw teacher notes into structured, professional daily diaries for parents.

### Target Audience:
- School Administrators & Principals
- Class Teachers & Subject Instructors
- Parents & Guardians

---

## 🚀 Live Deployed Application

- **Live URL:** [https://cambridge-automision.streamlit.app/](https://cambridge-automision.streamlit.app/)
- **GitHub Repository:** [https://github.com/khursheedahmed4u2010-create/Cambridge-Automision](https://github.com/khursheedahmed4u2010-create/Cambridge-Automision)

---

## ✨ Features List

1. **📊 Real-Time Analytics Dashboard:**
   - Synchronizes directly with Google Sheets (`Students_Master`).
   - Displays real-time metrics including total enrolled students, teacher assignments, and current fee statuses.
   - Interactive, searchable data table for quick administrative access.

2. **📋 Attendance Tracker & Instant WhatsApp Alerts:**
   - Class-wise student dropdown selection.
   - One-click attendance status logging (Present / Absent).
   - Automated creation of pre-formatted WhatsApp direct link (`https://wa.me/`) to instantly notify parents when a student is absent.

3. **🤖 AI Smart Diary & Notice Generator (Core AI Feature):**
   - Allows teachers to type rough, unstructured class notes or homework points.
   - Leverages **Google Gemini 1.5 Flash** to generate structured, polite, and emoji-enhanced WhatsApp diary notices in Roman Urdu/English mix.

---

## 🤖 The AI Feature & System Prompt

### AI Functionality:
The **AI Smart Diary Generator** takes brief, informal notes input by subject teachers and structures them into a parent-friendly format with appropriate greetings, clear subject breakdowns, homework guidelines, and school sign-offs.

### System Prompt Instructions Used:
```text
You are an expert school coordinator. Convert the following teacher's raw daily notes into a polite, professional, and clear WhatsApp message for parents in Urdu/English mix (Roman Urdu/Urdu).

Subject: {subject}
Raw Note: {raw_notes}

Make it structured with emojis, clear homework instructions, and polite greeting from Cambridge High School.
