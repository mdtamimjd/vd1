const express = require('express');
const ytDlp = require('yt-dlp-exec');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.post('/get-info', async (req, res) => {
    const videoUrl = req.body.url;

    if (!videoUrl) {
        return res.status(400).json({ error: 'URL is required' });
    }

    try {
        // yt-dlp options
        const options = {
            dumpSingleJson: true,
            noWarnings: true,
            noCallHome: true,
            preferFreeFormats: true,
            youtubeSkipDashManifest: true,
        };

        // Jodi cookies.txt thake, tobe seta add korbe
        if (fs.existsSync('cookies.txt')) {
            options.cookiefile = 'cookies.txt';
        }

        const info = await ytDlp(videoUrl, options);

        // Shudhu MP4 ebong Audio thaka formats filter kora
        const formats = info.formats
            .filter(f => f.ext === 'mp4' && f.vcodec !== 'none' && f.acodec !== 'none')
            .map(f => ({
                quality: f.format_note || 'HD',
                url: f.url,
                ext: f.ext
            }));

        res.json({
            title: info.title,
            thumbnail: info.thumbnail,
            duration: info.duration_string,
            formats: formats
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Failed to fetch video info. Try adding cookies.txt' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
