module Jekyll
    module Toolbox
      def keys(hash)
        hash.keys
      end
      def to_title_order(collection)
        result = collection.sort_by { |hsh| hsh["title"] }
        result
      end
    end
  end
  
  Liquid::Template.register_filter(Jekyll::Toolbox)