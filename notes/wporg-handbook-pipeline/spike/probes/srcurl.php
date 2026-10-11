<?php
$i = HelpHub_Spike_Importer::instance();
foreach ( array( "overview/README.md", "./overview/README.md", "../docs/overview/README.md", "/overview/README.md", "http://example.com/a.md", "https://github.com/o/r/blob/trunk/docs/a.md" ) as $s ) { echo str_pad( $s, 48 ), " => ", $i->generate_markdown_source_url( $s ), "\n"; }
