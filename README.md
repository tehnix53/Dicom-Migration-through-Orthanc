# Dicom-Migration-through-Orthanc
  GUI  to transfer large amounts of DICOM data to the remote server through Orthanc API

  To work, you need Orthanc installed on the local machine, with remote hosts, configured in json file.
  Pre-condition to sucess migration to remote host: test echo from local Orthanc toremote host is success status.

Aplicable for migrating a large amount of data to a remote DICOM server.

  in firs step - choose folder with .bin or .dcm or .dsr files.
  in second step push "confirm" button to start upload files to your local Orthanc. Wait, until progressbar is
reaches 100%.
  in thirst step push "show all" button to print all of your configured remote hosts. 
You need to copy or print name host your needed to "AE_Title" field.
  In fourthly push start button to send all images to remote host. Wait, until progressbar is reaches 100 %.
  In fifth, if you need it, drop all images from your local orthanc by pushing "clean" button. Wait, until progressbar
is reaches 100 %.
