#!/usr/bin/ruby

#require 'rubygems'
require 'hpricot'

bye_weeks = { 'Det' => '4', 'Ind' => '4', 'Mia' => '4', 'NE' => '4', 'NYG' => '4', 'Sea' => '4', 
              'Cle' => '5', 'NYJ' => '5', 'Oak' => '5', 'StL' => '5',
              'Buf' => '6', 'KC'  => '6', 'Pit' => '6', 'Ten' => '6',
              'Ari' => '7', 'Atl' => '7', 'Jac' => '7', 'Phi' => '7',
              'Chi' => '8', 'Cin' => '8', 'Den' => '8', 'GB'  => '8', 'Hou'  => '8', 'Min' => '8',
              'Car' => '9', 'NO'  => '9', 'SD'  => '9', 'SF'  => '9',
              'Bal' => '10', 'Dal' => '10', 'TB' => '10', 'Was' => '10' }

outfile = File.new("playerdata.csv", "w")

headers = ['Player','Team','Position','Bye','Projected','2007 Actual','Fan Pts','Passing Yds','Passing TD','Int','Sack','Rushing Yds','Rushing TD','Receiving Yds','Receiving TD','Ret TD','Misc 2pt','Fum Lost']

outfile.puts headers.join(',')

header_map = Hash.new
header_map['O'] = [nil, nil, nil, nil, nil, 'Projected','2007 Actual', nil, 'Passing Yds','Passing TD','Int','Sack','Rushing Yds','Rushing TD','Receiving Yds','Receiving TD','Ret TD','Misc 2pt','Fum Lost','Fan Pts']
header_map['K'] = [nil, nil, nil, nil, nil, 'Projected','2007 Actual', nil, nil, nil, nil, nil, nil, nil, 'Fan Pts']
header_map['DEF'] = [nil, nil, nil, nil, nil, 'Projected','2007 Actual', nil, nil, nil, nil, nil, nil, nil, nil, nil, 'Fan Pts']

max = { 'O' => 300, 'K' => 50, 'DEF'=> 50 }
players = Array.new

['O', 'K', 'DEF'].each do |pos|
    counter = 0
    while counter < max[pos]
        web_page = "http://football.fantasysports.yahoo.com/f1/27386/players?status=A&pos=#{pos}&cut_type=9&stat1=S_S_2007&sort=PR&count=#{counter}"

        doc = IO.popen("wget --load-cookies ~/.mozilla/firefox/*.default/cookies.txt -O - '#{web_page}'") { |f| Hpricot(f) }

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

