<!--
    XSLT transformation from RFC2629 XML format to Microsoft HTML Help TOC File

    Copyright (c) 2003 Julian F. Reschke (julian.reschke@greenbytes.de)

    placed into the public domain

    change history:

    2003-11-16  julian.reschke@greenbytes.de

    Initial release.
    
    2003-04-04  julian.reschke@greenbytes.de

    Add updated handling of references sections.
-->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:msxsl="urn:schemas-microsoft-com:xslt"
                xmlns:exslt="http://exslt.org/common"
                xmlns:myns="mailto:julian.reschke@greenbytes.de?subject=rcf2629.xslt"
                version="1.0"
                exclude-result-prefixes="msxsl exslt myns"
>

<xsl:param name="basename" />

<xsl:include href="rfc2629.xslt" />

<xsl:output indent="yes"/>

<xsl:template match="/" priority="9">
<html>
  <head>
    <!-- generator -->
    <meta name="generator" content="rfc2629toHhc.xslt $Id: rfc2629toHhc.xslt,v 1.13 2005/01/30 15:46:34 jre Exp $" />
  </head>
  <body>
    <object type="text/site properties">
        <param name="ImageType" value="Folder" />
        <param name="Window Styles" value="0x800025" />
    </object>
    <ul>
      <li>
        <object type="text/sitemap">
          <param name="Name" value="{/rfc/front/title}" />
          <param name="Local" value="{$basename}.html" />
        </object>
        <ul>
          <xsl:apply-templates mode="hhc" />
        </ul>
      </li>
    </ul>
  </body>
</html>
</xsl:template>

<xsl:template match="node()" mode="hhc">
  <xsl:apply-templates mode="hhc"/>
</xsl:template>

<xsl:template match="abstract" mode="hhc">
  <li>
    <object type="text/sitemap">
      <param name="Name" value="Abstract" />
      <param name="Local" value="{$basename}.html#{$anchor-prefix}.abstract" />
    </object>
  </li>
  <ul>
    <xsl:apply-templates mode="hhc"/>
  </ul>
</xsl:template>

<xsl:template match="note" mode="hhc">
  <li>
    <object type="text/sitemap">
      <param name="Name" value="{@title}" />
      <xsl:variable name="num"><xsl:number/></xsl:variable>
      <param name="Local" value="{$basename}.html#{$anchor-prefix}.note.{$num}" />
    </object>
  </li>
  <ul>
    <xsl:apply-templates mode="hhc"/>
  </ul>
</xsl:template>

<xsl:template match="section[@myns:unnumbered]" mode="hhc">
  <li>
    <object type="text/sitemap">
      <param name="Name" value="{@title}" />
      <param name="Local" value="{$basename}.html#{@anchor}" />
    </object>
  </li>
  <ul>
    <xsl:apply-templates mode="hhc"/>
  </ul>
</xsl:template>

<xsl:template match="section[not(@myns:unnumbered)]" mode="hhc">
  <xsl:variable name="sectionNumber"><xsl:call-template name="get-section-number" /></xsl:variable>
  <li>
    <object type="text/sitemap">
      <param name="Name" value="{$sectionNumber} {@title}" />
      <param name="Local" value="{$basename}.html#{$anchor-prefix}.section.{$sectionNumber}" />
    </object>
  </li>
  <ul>
    <xsl:apply-templates mode="hhc"/>
  </ul>
</xsl:template>


<xsl:template name="references-toc">

  <!-- distinguish two cases: (a) single references element (process
  as toplevel section; (b) multiple references sections (add one toplevel
  container with subsection) -->

  <xsl:variable name="number">
    <xsl:call-template name="get-references-section-number"/>
  </xsl:variable>

  <xsl:choose>
    <xsl:when test="count(/*/back/references) = 1">
      <xsl:for-each select="/*/back/references">
        <xsl:variable name="title">
          <xsl:choose>
            <xsl:when test="@title!=''"><xsl:value-of select="@title" /></xsl:when>
            <xsl:otherwise>References</xsl:otherwise>
          </xsl:choose>
        </xsl:variable>
      
        <li>
          <object type="text/sitemap">
            <param name="Name" value="{$number} {$title}" />
            <param name="Local" value="{$basename}.html#{$anchor-prefix}.references" />
          </object>
        </li>
      </xsl:for-each>
    </xsl:when>
    <xsl:otherwise>
      <!-- insert pseudo container -->    
      <li>
        <object type="text/sitemap">
          <param name="Name" value="{$number} References" />
          <param name="Local" value="{$basename}.html#{$anchor-prefix}.references" />
        </object>
        <ul>
          <!-- ...with subsections... -->    
          <xsl:for-each select="/*/back/references">
            <xsl:variable name="title">
              <xsl:choose>
                <xsl:when test="@title!=''"><xsl:value-of select="@title" /></xsl:when>
                <xsl:otherwise>References</xsl:otherwise>
              </xsl:choose>
            </xsl:variable>
          
            <xsl:variable name="sectionNumber">
              <xsl:call-template name="get-section-number" />
            </xsl:variable>
    
            <xsl:variable name="num">
              <xsl:number/>
            </xsl:variable>
    
            <li>
              <object type="text/sitemap">
                <param name="Name" value="{$sectionNumber} {$title}" />
                <param name="Local" value="{$basename}.html#{$anchor-prefix}.references.{$num}" />
              </object>
            </li>
          </xsl:for-each>
        </ul>
      </li>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="references" mode="hhc">

  <xsl:variable name="num">
    <xsl:choose>
      <xsl:when test="not(preceding::references)" />
      <xsl:otherwise>
        <xsl:text>.</xsl:text><xsl:number/>      
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <xsl:variable name="title">
    <xsl:choose>
      <xsl:when test="@title"><xsl:value-of select="@title" /></xsl:when>
      <xsl:otherwise>References</xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <li>
    <object type="text/sitemap">
      <param name="Name" value="{$title}" />
      <param name="Local" value="{$basename}.html#{$anchor-prefix}.references{$num}" />
    </object>
  </li>

</xsl:template>

<xsl:template match="back" mode="hhc">

  <!-- <xsl:apply-templates select="references" mode="hhc" /> -->
  <xsl:apply-templates select="*[not(self::references)]" mode="hhc" />
  <xsl:apply-templates select="/rfc/front" mode="hhc" />

  <xsl:if test="not($xml2rfc-private)">
    <!-- copyright statements -->
    <li>
      <object type="text/sitemap">
        <param name="Name" value="Intellectual Property and Copyright Statements" />
        <param name="Local" value="{$basename}.html#{$anchor-prefix}.ipr" />
      </object>
    </li>
  </xsl:if>

  <!-- insert the index if index entries exist -->
  <xsl:if test="//iref">
    <li>
      <object type="text/sitemap">
        <param name="Name" value="Index" />
        <param name="Local" value="{$basename}.html#{$anchor-prefix}.index" />
      </object>
    </li>
  </xsl:if>
</xsl:template>

<xsl:template match="front" mode="hhc">

  <xsl:variable name="title">
    <xsl:if test="count(author)=1">Author's Address</xsl:if>
    <xsl:if test="count(author)!=1">Author's Addresses</xsl:if>
  </xsl:variable>

  <li>
    <object type="text/sitemap">
      <param name="Name" value="{$title}" />
      <param name="Local" value="{$basename}.html#{$anchor-prefix}.authors" />
    </object>
  </li>
</xsl:template>

<xsl:template match="rfc" mode="hhc">
  <xsl:if test="not($xml2rfc-private)">
    <!-- Get status info formatted as per RFC2629-->
    <xsl:variable name="preamble"><xsl:call-template name="insertPreamble" /></xsl:variable>

    <!-- emit it -->
    <xsl:choose>
      <xsl:when test="function-available('msxsl:node-set')">
        <xsl:apply-templates select="msxsl:node-set($preamble)/node()" mode="hhc"/>
      </xsl:when>
      <xsl:when test="function-available('exslt:node-set')">
        <xsl:apply-templates select="exslt:node-set($preamble)/node()" mode="hhc"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="$preamble/node()" mode="hhc"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:if>
  
  <xsl:apply-templates select="front/abstract" mode="hhc"/>
  <xsl:apply-templates select="front/note" mode="hhc"/>

  <xsl:if test="$xml2rfc-toc">
    <bookmark xmlns="http://www.renderx.com/XSL/Extensions" internal-destination="{concat($anchor-prefix,'.toc')}">
      <bookmark-label>Table of Contents</bookmark-label>
    </bookmark>
  </xsl:if>

  <xsl:apply-templates select="middle|back" mode="hhc" />
</xsl:template>


<xsl:template match="middle" mode="hhc">

  <xsl:apply-templates mode="hhc"/>
  <xsl:call-template name="references-toc"/>>
</xsl:template>

   
</xsl:transform>