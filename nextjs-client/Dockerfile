# Start from the official Node.js 14 image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json before other files
# Utilise Docker cache to save re-installing dependencies if unchanged
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN npm install -g pnpm
RUN pnpm install

# Copy all files
COPY . .

# Build the project
RUN pnpm run build

# Expose the listening port
EXPOSE 3000

# Run npm start script
CMD ["pnpm", "run", "start"]