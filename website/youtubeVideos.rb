require 'json'
require 'net/http'
require 'uri'

puts "Fetching youtube videos for webinars page"

def fetchVideos (videos, error, nextPageToken)
  uri = URI("https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=UUlROK3yIuIyJWmt-gnkAjlQ&key=AIzaSyCKS2_U1c9NGRlcobOjN9MEpV1WGGWVHSA#{ "&pageToken=#{nextPageToken}" if nextPageToken }")
  res = Net::HTTP.get_response(uri)

  if res.code == "200"
    body = JSON.parse(res.body)

    body['items'].each do |video|
      videos << { title: video['snippet']['title'], videoId: video['snippet']['resourceId']['videoId'], type: 'Video' }
    end

    return body['nextPageToken']
  end

  error = true
  puts "Error fetching youtube data: #{res.body}"

  return nil
end

begin
  videos = []
  error = false

  response = fetchVideos(videos, error, nil)
  while response
    response = fetchVideos(videos, error, response)
  end

  if !error
    puts "Updated videos data in _data directory"
    File.write("_data/webinar-videos.json", videos.to_json)
  end
rescue Timeout::Error, Errno::EINVAL, Errno::ECONNRESET, EOFError, Net::HTTPBadResponse, Net::HTTPHeaderSyntaxError, Net::ProtocolError => e
end
