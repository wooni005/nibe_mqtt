#!/usr/bin/perl

use strict;
use warnings;
use JSON;
use LWP::Authen::OAuth2;

# File-scope variables, available to Main Program and Subroutines
our $filename = $ENV{ "HOME" }.'/.NIBE_Uplink_API_Tokens.json';

# Subroutine to save Access and Refresh tokens when those change
sub save_tokens {
    my $token_string = shift;
    open( my $fh, '>', $filename );
    print $fh $token_string;
    close $fh;
}
# Main Program

# Local variables
my $token_string;
my $url;
my $response;
my $decoded;

# Read saved token_string from file
open( my $fh, '<', $filename )
    or die "Could not open file $filename: $!";
$token_string = <$fh>;
chomp $token_string;
close( $fh );

# Construct the OAuth2 object
my $oauth2 = LWP::Authen::OAuth2->new(
    client_id => '9b1e683e2c904adfb52313b4a327b634',
    client_secret => '8YL79duUZWfQAgVdjQmuNZczAtaed5fawULKfhcPzQM=',
    token_endpoint => 'https://api.nibeuplink.com/oauth/token',
    redirect_uri => 'https://www.marshflattsfarm.org.uk/nibeuplink/oauth2callback/index.php',
    request_required_params => [ 'redirect_uri', 'state', 'scope', 'grant_type', 'client_id', 'client_secret', 'code' ],
    scope => 'READSYSTEM',
    token_string => $token_string,
    save_tokens => \&save_tokens
);

# Make a simple NIBE Uplink API call - Get the Systems for this Account
$url = "https://api.nibeuplink.com/api/v1/systems";
$response = $oauth2->get( $url );
if ( $response->is_error ) { print $response->error_as_HTML }
if ( $response->is_success ) {
    $decoded = decode_json( $response->content );
    # Expect $decoded to be a Reference to a Hash
    my $objects = $decoded->{ 'objects' };
    # Expect $objects to be a Reference to an Array of Hashes
    for my $hashref ( @ { $objects } ) {
        my $system = $hashref->{ 'systemId' };
        print "systemId = ".$system."\n";
    }
}

exit;
