#!/usr/bin/perl

use strict;
use warnings;
use LWP::Authen::OAuth2;

our $filename = $ENV{ "HOME" }.'/.NIBE_Uplink_API_Tokens.json';

sub save_tokens {
    my $token_string = shift;
    open( my $fh, '>', $filename );
    print $fh $token_string;
    close $fh;
}

my $oauth2 = LWP::Authen::OAuth2->new(
    client_id => '9b1e683e2c904adfb52313b4a327b634',
    client_secret => '8YL79duUZWfQAgVdjQmuNZczAtaed5fawULKfhcPzQM=',
    token_endpoint => 'https://api.nibeuplink.com/oauth/token',
    redirect_uri => 'https://www.marshflattsfarm.org.uk/nibeuplink/oauth2callback/index.php',
    request_required_params => [ 'redirect_uri', 'state', 'scope', 'grant_type', 'client_id', 'client_secret', 'code' ],
    scope => 'READSYSTEM',
    save_tokens => \&save_tokens
);

print "Create a new Authorization Code and enter (copy-and-paste) it here\n";
my $code = <STDIN>;
chomp $code;

$oauth2->request_tokens(
    code=> $code,
    state => '2c2a9286312342a9b9364bd8e4ee388d'
);

exit;

