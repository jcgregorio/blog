<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
	xmlns="http://www.w3.org/1999/xhtml"
	xmlns:atom="http://purl.org/atom/ns#">

	<xsl:template match="atom:feed">
		<example>
			<title>
				<xsl:apply-templates select="atom:title"/>
			</title>
		</example>
	</xsl:template>

	<xsl:template match="atom:title">
		<xsl:value-of select="text()"/>
	</xsl:template>

</xsl:stylesheet>
