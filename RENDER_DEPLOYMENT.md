# Deploying Forest Temperature Monitor to Render.com

Follow these steps to deploy your Forest Temperature Monitoring System on Render.com:

## Step 1: Set Up Render Account
1. Create an account on [Render.com](https://render.com/)
2. Verify your email and log in

## Step 2: Connect Your GitHub Repository
1. Click on "New" button in the Render dashboard
2. Select "Web Service"
3. Choose "Connect GitHub"
4. Select your repository: `PiyushJimiwal/Forest-temperature-monitor`

## Step 3: Configure the Web Service
1. **Name**: `forest-temperature-monitor` (or choose your preferred name)
2. **Environment**: `Python 3`
3. **Region**: Choose the region closest to you
4. **Branch**: `main`
5. **Build Command**: 
   ```
   pip install -r requirements.txt.github
   ```
6. **Start Command**: 
   ```
   streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
7. **Plan**: Free (or choose paid for more resources)

## Step 4: Advanced Settings
1. Click on "Advanced" settings
2. Set **Health Check Path** to `/`
3. Leave everything else as default

## Step 5: Create and Deploy
1. Click "Create Web Service"
2. Wait for the build and deployment process to complete

## Step 6: Access Your Application
1. Once deployed, Render will provide a URL to access your application
2. Click on the provided URL to open your Forest Temperature Monitoring System

## Troubleshooting
If you encounter any errors during deployment:

1. Check the build logs on Render for any dependency conflicts
2. Make sure the correct requirements file is being used (`requirements.txt.github`)
3. Verify that your application runs correctly locally

## Important Notes
- The free tier of Render will spin down with inactivity, which can cause a delay when someone visits your site after a period of inactivity
- For production use, consider upgrading to a paid plan for better performance and uptime