# ✅ Use official Python base image
FROM python:3.10

# ✅ Set working directory inside the container
WORKDIR /app

# ✅ Copy all OpenMail files
COPY . .

# ✅ Install Flask dependencies
RUN pip install flask requests

# ✅ Expose Flask port for NAT mapping
EXPOSE 5001

# ✅ Start Flask
CMD ["python", "backend/home_service.py"]
