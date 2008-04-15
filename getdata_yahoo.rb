#!/usr/bin/ruby

require 'rubygems'
require 'hpricot'

bye_weeks = { 'Jac' => '4', 'NO'  => '4', 'Ten' => '4', 'Was' => '4', 
              'Cin' => '5', 'Min' => '5', 'Oak' => '5', 'Phi' => '5',
              'Buf' => '6', 'Den' => '6', 'Det' => '6', 'Ind' => '6', 'Pit' => '6', 'SF'  => '6',
              'Car' => '7', 'Cle' => '7', 'GB'  => '7', 'SD'  => '7',
              'Ari' => '8', 'Atl' => '8', 'Bal' => '8', 'Dal' => '8', 'KC'  => '8', 'Sea' => '8',
              'Chi' => '9', 'Mia' => '9', 'NYG' => '9', 'StL' => '9',
              'Hou' => '10', 'NE' => '10', 'NYJ' => '10', 'TB' => '10' }

outfile = File.new("playerdata.csv", "w")

headers = ['Player','Team','Position','Bye','Projected','2006 Actual','Fan Pts','Passing Yds','Passing TD','Int','Rushing Yds','Rushing TD','Receiving Yds','Receiving TD','Ret TD','Misc 2pt','Fum Lost']

outfile.puts headers.join(',')

header_map = Hash.new
header_map['O'] = [nil, nil, nil, nil, nil, 'Projected','2006 Actual','Passing Yds','Passing TD','Int','Rushing Yds','Rushing TD','Receiving Yds','Receiving TD','Ret TD','Misc 2pt','Fum Lost','Fan Pts']
header_map['K'] = [nil, nil, nil, nil, nil, 'Projected','2006 Actual', nil, nil, nil, nil, nil, nil, 'Fan Pts']
header_map['DEF'] = [nil, nil, nil, nil, nil, 'Projected','2006 Actual', nil, nil, nil, nil, nil, nil, nil, 'Fan Pts']

max = { 'O' => 300, 'K' => 50, 'DEF'=> 50 }
players = Array.new

['O', 'K', 'DEF'].each do |pos|
    counter = 0
    while counter < max[pos]
        web_page = "http://football.fantasysports.yahoo.com/f1/269546/players?status=ALL&pos=#{pos}&cut_type=9&stat1=S_S_2006&sort=PR&count=#{counter}"

        doc = IO.popen("wget --load-cookies ~/.mozilla/firefox/fbbk7z3c.default/cookies.txt -O - '#{web_page}'") { |f| Hpricot(f) }

        doc.search("table.teamtable/tbody/tr").each do |row|
            data = Hash.new
            row.search("td").each_with_index do |col, i|
                if col['class'] == "player first"
                    data['Player'] = col.at("div/a/").inner_text
                    tmp = col.at("div.detail/span").inner_text
                    if tmp =~ /\((\w+) - (\w+)\)/
                        data['Team'] = $1
                        data['Position'] = $2
                        data['Bye'] = bye_weeks[$1]
                    end
                    if col.at("div.detail/span.status")
                        data['Player'] = data['Player'] + " (" + col.at("div.detail/span.status").inner_text + ")"
                    end
                else
                    data[header_map[pos][i]] = col.inner_text if header_map[pos][i] != nil
                end
            end
            players.push(data)
        end

        counter = counter + 25
    end
end

players.sort! { |a, b| a['Projected'].to_i <=> b['Projected'].to_i }

players.each do |player|
    values = Array.new
    headers.each { |header| values.push(player[header] || '-') }
    outfile.puts values.join(',')
end

