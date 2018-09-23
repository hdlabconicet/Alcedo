
work = Collection.last.works[1]
thompson_pages = {}
 work.pages[3..575].each_with_index {|pg,i| words=pg.source_text.scan(/([A-Z]{2,})/).each {|cap| thompson_pages[cap.first] ||= i+4 } unless  pg.source_text.blank? }
 alcedo_text = File.read('/home/benwbrum/dev/clients/delrio/alcedo/mine/Alcedo/FTP/alcedo-1.txt');0
alcedo_lines = alcedo_text.split("\n");0

current_page = 3
# AMERICA is 7 pages
# BRAZIL is 30 pages
# CHILE is 51 pages
MAX_PAGES_PER_ENTRY = 51

paginated = {}
unassigned = []
alcedo_lines.each_with_index do |line,i|
  if line.match /([A-Z]{2,})/
    headword = $1
    tentative_page = thompson_pages[headword]
#    print "#{i}\tthompson_pages[#{headword}] => #{thompson_pages[headword]}\n"
    if tentative_page && headword.match(/^[A-C]/)
#      print "#{i}\t#{headword}\t#{tentative_page}\t#{(tentative_page.to_i - current_page.to_i)}\n"
      if tentative_page.to_i > current_page.to_i 
        if (tentative_page.to_i - current_page.to_i) <= MAX_PAGES_PER_ENTRY
          print "#{i}\tcurrent_page #{current_page} -> #{tentative_page}\n"
          current_page = tentative_page
        else
          print "#{i}\tSKIP\t#{headword.rjust(9,' ')}\t#{tentative_page}\t#{(tentative_page.to_i - current_page.to_i)}\n"
        end
      end
    end
  end
  paginated[current_page] ||= []
#  print "#{i}\tadding to page #{current_page}\t(size=#{paginated[current_page].size})\n"
  paginated[current_page] << line
end;0

paginated.keys.each do |page_no|
  filename = page_no.to_s.rjust(3,"0") + ".txt"
  outfile = File.join('/home/benwbrum/dev/clients/delrio/alcedo/mine/Alcedo/FTP/v1', filename)
  File.write(outfile, paginated[page_no].join("\n"))
end


trans_url = "https://fromthepage.lib.utexas.edu/benwbrum/latam-digital-edition-and-gazetteer/alcedo-thompson-1/translate/"
github_url = "https://raw.githubusercontent.com/hdcaicyt/Alcedo/master/FTP/v1/"
links = []
paginated.keys.each do |page_no|
  filename = page_no.to_s.rjust(3,"0") + ".txt"
  page = work.pages.where(:title => page_no.to_s).first
  if page
    links << "#{page_no} []TODOTODOTODO[#{trans_url}#{page.id}](#{github_url}#{filename})"
  end
end



transcribe= "https://fromthepage.lib.utexas.edu/benwbrum/latam-digital-edition-and-gazetteer/alcedo-thompson-1/transcribe"
github_url = "https://raw.githubusercontent.com/benwbrum/Alcedo/master/FTP/thompson/v1"

markdown = ""
work.pages.each do |page|
  filename = page.title.rjust(3,"0") + ".txt"
  file_link = "#{github_url}/#{filename}"
  ftp_link = "#{transcribe}/#{page.id}"
  markdown << "* #{page.title} [copy](#{file_link}) [paste](#{ftp_link})\n"
end
File.write("/home/benwbrum/dev/clients/delrio/alcedo/mine/Alcedo/FTP/thompson/README.md", markdown)

# patterns: always follow a newline


[ARKANSAS, or Arkensas,
ARJONA,
[ARIZIBO,
ARITAGUA,
ARISMENDI, Santiago de,
 
BASSE VI LLE,

page = work.pages[70]
paras =  page.source_text.split(/\n\n/)
LEAD_CONTEXT = [
  'township of ',
  'government of ',
  'island of ',
  'colony of ',
  'coast of ',
  'province of ',
  'district of ',
  'corregimiento of ',
  'county of ',
  'state of ',
  'kingdom of ',
  'captainship of ',
  'major of ',
  'mayor of '
]
REPLACEMENTS={
  'Brazil' => '[[Brasil|Brazil]]',
  'Tierra Firme' => '[[Tierra Firme]]',
  '[[Tierra]] Firme' => '[[Tierra Firme]]',
  'Peru' => '[[Peru]]',
  '[[[[Peru]]]]' => '[[Peru]]',
  'Nueva Espana' => '[[Nueva España]]',
  'Nueva España' => '[[Nueva España]]',
  '[[Nueva]] Espana' => '[[Nueva España]]',
  '[[Nueva]] España' => '[[Nueva España]]',
  '[[[[Nueva España]]]]' => '[[Nueva España]]',
  '[[Nueva]] Vizcaya' => '[[Nueva Vizcaya]]'
}


work.pages.each do |page|
  filename = page.title.rjust(3,"0") + ".txt"
  outfile = File.join('/home/benwbrum/dev/clients/delrio/alcedo/mine/Alcedo/FTP/thompson/v1', filename)

  unless page.source_text.blank?
    paras =  page.source_text.split(/\n\n/)

    cleaned = ""
    paras.each do |para| 
      if para.match(/\A\[?([A-Z][^\.,]*)/m)
        raw = $1
        if raw.match(/[A-Z ]{2,}/)
          replacement = "==[[#{raw.titleize}|#{raw}]]=="
        else
          replacement = "==[[#{raw}]]=="
        end
        para = para.sub(raw, replacement)
      end
    # para = para.sub(/\A\[?([A-Z][^\.,]*)/m, "==[[#{$1.titleize}|\\1]]==") 
      LEAD_CONTEXT.each do |context|
        para = para.sub(/(#{context})(([A-Z][A-Za-zñ']+)+)/, '\1[[\2]]')
      end
      para = para.gsub(/ \]\]/, ']]') if para

      REPLACEMENTS.each_pair do |search, replace|
        para = para.sub(search, replace)
      end
      cleaned += para
      cleaned += "\n\n"
    end

    File.write(outfile, cleaned)
  end
end



