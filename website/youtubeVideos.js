const fs = require('fs')
const https = require('https')

console.log('Fetching youtube videos')

try {
https.get('https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=UUlROK3yIuIyJWmt-gnkAjlQ&key=AIzaSyCKS2_U1c9NGRlcobOjN9MEpV1WGGWVHSA', (res) => {
  let data = ""

  res.on("data", chunk => data += chunk)

  res
    .on("end", () => {
      let videos = JSON.parse(data).items.map(video => {
        const { title, description, resourceId } = video.snippet
        return {
          title,
          description,
          videoId: resourceId.videoId,
          type: 'Video'
        }
      })

      fs.writeFileSync('_data/webinar-videos.json', JSON.stringify(videos))
      console.log('Updated videos data')
    })
    .on("error", error => console.log("Error while fetching youtube data: ", error))
})
} catch (err) {
  console.log('Error while fetching youtube data: ', err)
}