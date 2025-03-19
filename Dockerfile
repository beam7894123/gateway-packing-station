FROM node:22

# Set the working directory
WORKDIR /usr/src/app

# Install required dependencies for Puppeteer and Chromium
RUN apt-get update && apt-get install -y \
    chromium

# Set the environment variable to skip Chromium download in Puppeteer
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Ensure Prisma Client is generated
RUN npx prisma generate

# Expose the application port
EXPOSE 3000

# Command to run the application
CMD ["npm", "start"]
