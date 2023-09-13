require 'json'
require 'net/http'
require 'uri'

puts "Fetching youtube videos for webinars page"

def fetchVideos (videos, errors, nextPageToken)
  uri = URI("https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=UUlROK3yIuIyJWmt-gnkAjlQ&key=#{ARGV[0]}#{ "&pageToken=#{nextPageToken}" if nextPageToken }")
  res = Net::HTTP.get_response(uri)

  if res.code == "200"
    body = JSON.parse(res.body)

    body['items'].each do |video|
      videos << { title: video['snippet']['title'], videoId: video['snippet']['resourceId']['videoId'], type: 'Video' }
    end

    return body['nextPageToken']
  end

  errors << res.body
  puts "Error fetching youtube data: #{res.body}"

  return nil
end

begin
  videos = []
  errors = []

  response = fetchVideos(videos, errors, nil)
  while response
    response = fetchVideos(videos, errors, response)
  end

  if errors.length == 0
    puts "Updated videos data in _data directory"
    File.write("./_data/webinar-videos.json", videos.to_json)
  end
rescue Timeout::Error, Errno::EINVAL, Errno::ECONNRESET, EOFError, Net::HTTPBadResponse, Net::HTTPHeaderSyntaxError, Net::ProtocolError => e
end
