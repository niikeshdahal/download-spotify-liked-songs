# Download spotify liked songs
This guide will walk you through the necessary steps to set this up and authorize it with the Spotify API. This process involves creating a Spotify Developer application, generating the necessary credentials, and configuring your local environment.

## Prerequisites

- A Spotify account.
- `curl` installed on your command line.
- Python and `pip` installed .

---

### Step 1: Create a Spotify Developer App

First, you need to register an application on the Spotify Developer Dashboard.

1.  **Go to the Spotify Developer Dashboard:** [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) and log in.
2.  **Create an App:** Click the "Create App" button. Give your application a name and description, then agree to the terms.
3.  **Find Your Credentials:** Once your app is created, you will see your **Client ID**. Click "Show client secret" to see your **Client Secret**. Keep these two values safe; you will need them later.
4.  **Set the Redirect URI:** Click "Edit Settings". In the "Redirect URIs" section, add a URI. For local testing, `http://localhost:8888/callback` is a common choice. **You must add a URI here, and it must exactly match the one you use in the next steps.** Click "Save".

---

### Step 2: Get Your Authorization Code

Next, you need to get a temporary authorization code from Spotify by having a user (yourself) grant permission to your app.

1.  **Construct the Authorization URL:** Copy the following URL and replace `YOUR_CLIENT_ID` with your actual Client ID from the Spotify dashboard.

    ```
    [https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8888%2Fcallback&scope=user-library-read](https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8888%2Fcallback&scope=user-library-read)
    ```

    > **Note:** The `redirect_uri` in this URL (`http%3A%2F%2Flocalhost%3A8888%2Fcallback`) must be one of the URIs you registered in Step 1.

2.  **Authorize the App:** Paste the completed URL into your browser. You will be asked to log in to Spotify and then grant permission to your app.
3.  **Copy the Code:** After you agree, you will be redirected to a page that may show an error (this is normal). Look at the URL in your browser's address bar. It will now contain a `code` parameter. The URL will look something like this:
    `http://localhost:8888/callback?code=AQ...BkWtQ`

    Copy the long string of characters that comes after `code=`. This is your temporary authorization code.

---

### Step 3: Get Your Refresh Token

Now, you will exchange the temporary code for a permanent `refresh_token`. This is done via a `curl` command in your terminal.

1.  **Send the `curl` Request:** Open your terminal and run the following command. Replace the placeholder values with your actual information.

    ```bash
    curl -X POST \
      [https://accounts.spotify.com/api/token](https://accounts.spotify.com/api/token) \
      -H 'Authorization: Basic YOUR_BASE64_ENCODED_CLIENT_ID_AND_SECRET' \
      -d 'grant_type=authorization_code' \
      -d 'code=AUTHORIZATION_CODE_FROM_CALLBACK' \
      -d 'redirect_uri=http%3A%2F%2Flocalhost%3A8888%2Fcallback'
    ```

3.  **Save Your Refresh Token:** The command will return a JSON object containing an `access_token` and, most importantly, a `refresh_token`. Copy the `refresh_token` value and save it.

---

### Step 4: Configure Your Local Environment

Create a `.env` file in the root directory of the project to store your secrets. This file should never be committed to Git.

1.  Create a file named `.env`.
2.  Add your credentials to the file in the following format:

    ```
    SPOTIFY_CLIENT_ID=your_client_id
    SPOTIFY_CLIENT_SECRET=your_client_secret
    SPOTIFY_REFRESH_TOKEN=your_refresh_token
    ```

---

### Step 5: Run the Project

Now you are ready to run the project.

1.  **Install Dependencies:** Open your terminal in the project root and install the required packages.
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Script:** Execute the main Python scripts.
    ```bash
    python getLikedSongs.py
    python downloader.py
    ```

The script will now use the credentials in your `.env` file to authenticate with the Spotify API and donwnload all your liked songs.

