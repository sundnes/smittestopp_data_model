#!/usr/bin/perl
use POSIX;

### this script reads the initial contact data, filter out contacts that are deemed unrisky either because of low BLE signal strength or short duration###
## It takes four commandline arguments: the list of filkes to be read, min RSSI threshold, min duration threshold and a final argument for naming output files##    
$files=$ARGV[0];
$att_th = $ARGV[1];
$dur_th = $ARGV[2];
$suffix = $ARGV[3];


open(A,"$files");

%contacts = ();
%length = ();
%att = ();
%plats = ();
%days_wm=();
foreach $file_a(<A>)
{
    chomp($file_a);
    ## This part reads the input files and stores the contacts that each device had, along with the number of days that a contact was observed on, the highest RSSI and the longest duration across all days      	
    ## the input file is a comma delimited file with ten values in each line that summarize daily interactions between two device>
    ## these fields are the day, an identifier for the first device, 
    ### identifer for the second device, the paltforms of the first and second device (ios or android),
    ### the time difference between the first and last measured RSSI, highest RSSI, average RSSI, number of measurements

    %seen=();
    open(F,"gzip -dc $file_a |");
    @name = split('\/',$file_a);
    ($lead,$res) = split('\.',$name[@name-1]);
    $my_day = 0;
    
    while(<F>)
    {
        chomp($_);
        $_ =~ s/\s*$//;
        $a_id =~ s/\s*$//;
        $b_id =~ s/\s*$//;
        $max_att =~ s/\s*$//;
        $dur =~ s/\s*$//;
        $plt_a =~ s/\s*$//;
        $plt_b =~ s/\s*$//;
        ($day,$a_id,$b_id,$plt_a,$plt_b,$dur,$max_att,$avg_att,$pairings)=split('\,',$_);
        $my_day = $day;
        next if($dur<$dur_th || $max_att<$att_th);
        $plats{$a_id} = $plt_a;
        $plats{$b_id} = $plt_b; 
        $days_wm{$a_id}{$day} = 1;
        $days_wm{$b_id}{$day} = 1;
        if(! exists $seen{$b_id}{$a_id})
        {
            $contacts{$a_id}{$b_id} +=1;
            $contacts{$b_id}{$a_id} +=1;
            $seen{$a_id}{$b_id} =1;
        }
        if(exists $length{$a_id}{$b_id})
	{
	     if($length{$a_id}{$b_id}<$dur)
	     {
		$length{$a_id}{$b_id} = $dur;
		$length{$b_id}{$a_id} = $dur;	
	     }			
        }
	else
	{
	     $length{$a_id}{$b_id} = $dur;
             $length{$b_id}{$a_id} = $dur;	
        }
        if(exists $att{$a_id}{$b_id})
        { 
             if($att{$a_id}{$b_id}<$max_att)
             { 
                $att{$a_id}{$b_id} = $max_att;
                $att{$b_id}{$a_id} = $max_att;
             }
        }
        else
        {
	     $att{$a_id}{$b_id} = $max_att;
             $att{$b_id}{$a_id} = $max_att;	 
        }
    }
}

$f_a = 'links-'.$suffix.'.txt';
open(OUTA,">>$f_a");
## this part compares the common neighbours for every pair of devices that were in contact,
## computes three similarity metric: Jaccard, Sorensen and Adamic-adar indexes,
## finally it saves the summary statistics above along with information on similarity and the three metrics.      
foreach $dev_a(keys %contacts)
{
    $deg_a = keys %{$contacts{$dev_a}};
    
    foreach $dev_b(keys %{$contacts{$dev_a}})
    {
        $deg_b = keys %{$contacts{$dev_b}};
        $common = 0;
        $jaccard = 0;
        $sor = 0;
        $aa = 0; 
        foreach $dev_c(keys %{$contacts{$dev_b}})
        {
                if(exists $contacts{$dev_a}{$dev_c})
                {
			++$common;
                        $deg_c = keys %{$contacts{$dev_c}}; 
                        $aa = $aa +(1/log($deg_c));
                } 
        }     
        $jaccard = $common/($deg_a+$deg_b-$common);
        $sor = $common/($deg_a+$deg_b);
	$num_contacts = $contacts{$dev_a}{$dev_b};
        $plt_a = $plats{$dev_a};
        $plt_b = $plats{$dev_b};
        $dur = $length{$dev_a}{$dev_b};
        if(exists $att{$dev_a}{$dev_b})
        {
        	$highest_att = $att{$dev_a}{$dev_b};
        	$d_a = keys %{$days_wm{$dev_a}};
        	$d_b = keys %{$days_wm{$dev_b}}; 
        	$overlap = 0;  
        	foreach $day(keys %{$days_wm{$dev_a}})
        	{
			if(exists $days_wm{$dev_b}{$day}){++$overlap;}
		} 
        	print OUTA "$dev_a\t$dev_b\t$num_contacts\t$plt_a\t$plt_b\t$dur\t$highest_att\t$d_a\t$d_b\t$overlap\t$deg_a\t$deg_b\t$common\t$jaccard\t$sor\t$aa\n";
        }   
    }
    
}

close OUTA;
            

