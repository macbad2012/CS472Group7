# Web of Trust script - Stephen Woerner 
#
# Input: address - url to be verified by WoT (or just the domain)
# Output: prints domain, rating, and confidence values to file "wotscore.txt" 
# WOT API Key 69429eaef0f3cea5e334f84c5792bb521e81de5c

require LWP::UserAgent;

$address = $ARGV[0];
$domain = $address =~ /(?:.*\:\/\/)?(?:www.)?([^\/]+)(?:.*)/; #Parse domain 
$output = "$$domain";
$request = "http://api.mywot.com/0.4/public_link_json2?hosts=$output/&callback=process&key=69429eaef0f3cea5e334f84c5792bb521e81de5c";
my $ua = LWP::UserAgent->new;
$ua->timeout(10);
$ua->env_proxy;
my $response = $ua->get($request);
if ($response->is_success) {
    my ($rating, $confidence) = $response->decoded_content =~ /\"0\":\s+\[\s*(\d+),\s*(\d+)\s*\]/; #Parses out rating and confidence ratings
    open(my $fh, '>', 'wotscore.txt');
    print $fh $output;
    print $fh "\n$rating\n$confidence";
    close $fh; 
}

else {
    die 'Failed: response was not successful'
}

#Note: This is my first pearl script, there may be errors or bad practices