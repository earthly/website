module Jekyll
  module UtilFilter
    def raise_error(msg)
      bad_file = @context.registers[:page]['path']
      err_msg = "On #{bad_file}: #{msg}"
      raise err_msg
    end
    def print(msg)
      puts msg
    end
  end
end

Liquid::Template.register_filter(Jekyll::UtilFilter)
