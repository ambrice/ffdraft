#!/usr/bin/ruby

#require 'rubygems'
require 'hpricot'

bye_weeks = { 'Ari' => '4', 'Atl' => '4', 'Car' => '4', 'Phi' => '4',
              'Chi' => '5', 'GB'  => '5', 'NO'  => '5', 'SD'  => '5',
              'Dal' => '6', 'Ind' => '6', 'Mia' => '6', 'SF'  => '6',
              'Bal' => '7', 'Den' => '7', 'Det' => '7', 'Jac' => '7', 'Sea' => '7', 'Ten' => '7',
              'Cin' => '8', 'KC'  => '8', 'NE'  => '8', 'Pit' => '8', 'TB'  => '8', 'Was' => '8',
              'Buf' => '9', 'Cle' => '9', 'Min' => '9', 'NYJ' => '9', 'Oak' => '9', 'StL' => '9',
              'Hou' => '10', 'NYG' => '10' }

outfile = File.new("playerdata.csv", "w")

headers = ['Player','Team','Position','Bye','Projected','2008 Actual','Fan Pts','Passing Yds','Passing TD','Int','Sack','Rushing Yds','Rushing TD','Receiving Yds','Receiving TD','Ret TD','Misc 2pt','Fum Lost']

outfile.puts headers.join(',')

header_map = Hash.new
header_map['O'] = [nil, nil, nil, nil, nil, 'Projected','2008 Actual', nil, 'Passing Yds','Passing TD','Int','Sack','Rushing Yds','Rushing TD','Receiving Yds','Receiving TD','Ret TD','Misc 2pt','Fum Lost','Fan Pts']
header_map['K'] = [nil, nil, nil, nil, nil, 'Projected','2008 Actual', nil, nil, nil, nil, nil, nil, nil, 'Fan Pts']
header_map['DEF'] = [nil, nil, nil, nil, nil, 'Projected','2008 Actual', nil, nil, nil, nil, nil, nil, nil, nil, nil, 'Fan Pts']

max = { 'O' => 300, 'K' => 50, 'DEF'=> 50 }
players = Array.new

['O', 'K', 'DEF'].each do |pos|
    counter = 0
    while counter < max[pos]
        web_page = "http://football.fantasysports.yahoo.com/f1/373893/players?status=A&pos=#{pos}&stat1=S_S_2008&sort=PR&count=#{counter}"

        doc = IO.popen("wget --load-cookies ~/cookies.txt -O - '#{web_page}'") { |f| Hpricot(f) }

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

