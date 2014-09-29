# OnApp Roles Import/Export Scripts

** Warning: ** Please only import and export roles within the same version of OnApp. Do not use the same role file between versions as permission changes between versions of OnApp will cause incorrect permissions to be set for your roles. 

## Exporting Roles

The export script (**onapp_export_role.py**) can be executed as follows:

    python onapp_export_role.py <host> <user> <pass> <role-id>

An example of this command to download Role ID 20 from the http://mycloud.com OnApp Control Panel:

    python onapp_export_role.py http://mycloud.com admin password 20
    
This will create a file titled `20.role.json`. 

You can also use your Email Address and API Key as the authentication method as follows

    python onapp_export_role.py http://mycloud.com 'admin@email.com' api_key 20

## Importing a Role

The import script (**onapp_import_role.py**) can be executed as follows:

    python onapp_import_role.py <host> <user> <pass> <role-file> <new-role-label>

An example of this command to upload a role file `20.role.json` to the  http://mycloud.com OnApp Control Panel:

    python onapp_import_role.py http://mycloud.com admin password 20.role.json 'New Role'
    
This will import the role from the file `20.role.json` and give the new role a label of 'New Role'. Please note, Role labels need to be unique. You may get a 422 Unprocessible Entity error if you try to import a role which has the same label as an existing role.

## Requirements

These scripts have been tested on Python 2.7.5 running on Mac OSX. They don't have any external dependencies beyond Python and should work on any system. Tested on an OnApp 3.3 Cloud but should work on any OnApp 3.+ Cloud.

## License

> IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
