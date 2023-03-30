module Jekyll
  module Toolbox
    class IncludeHtmlTag < Jekyll::Tags::IncludeTag
      def render(context)
        site = context.registers[:site]
        page = context.registers[:page]

        # Resolve the include's file path
        dir = File.join(site.source, "_includes")
        file_path = File.expand_path(File.join(dir, @file))

        # Read the content of the included file and remove leading whitespace from each line
        content = File.read(file_path)
        stripped_content = content.gsub(/^[ \t]+/, '')

        # Create a new Liquid Template with the stripped content
        partial = Liquid::Template.parse(stripped_content)

        # Render the template using the current context and merge the included variables
        context.stack do
          context['include'] = parse_params(context) if @params
          partial.render!(context)
        end
      end
    end
  end
end

Liquid::Template.register_tag("include_html", Jekyll::Toolbox::IncludeHtmlTag)