<!--
    Strip rfc2629.xslt extensions, generating XML input for MTR's xml2rfc

    Copyright (c) 2006-2007, Julian Reschke (julian.reschke@greenbytes.de)
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of Julian Reschke nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
-->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0"
                xmlns:ed="http://greenbytes.de/2002/rfcedit"
                xmlns:x="http://purl.org/net/xml2rfc/ext"
                xmlns:xhtml="http://www.w3.org/1999/xhtml"
                exclude-result-prefixes="ed x xhtml"
>

<!-- re-use some of the default RFC2629.xslt rules -->
<xsl:import href="rfc2629.xslt"/>

<!-- undo strip-space decls -->
<xsl:preserve-space elements="*"/>

<!-- generate DTD-valid output, override all values imported from rfc2629.xslt -->
<xsl:output doctype-system="rfc2629.dtd" doctype-public="" method="xml" version="1.0" encoding="UTF-8" cdata-section-elements="artwork" />

<!-- kick into cleanup mode -->
<xsl:template match="/">
  <xsl:text>&#10;</xsl:text>
  <xsl:comment>
    This XML document is the output of clean-for-DTD.xslt; a tool that strips
    extensions to RFC2629(bis) from documents for processing with xml2rfc.
</xsl:comment>
  <xsl:apply-templates select="/" mode="cleanup"/>
</xsl:template>

<!-- rules for identity transformations -->

<xsl:template match="processing-instruction()" mode="cleanup">
  <xsl:text>&#10;</xsl:text>
  <xsl:copy><xsl:apply-templates select="node()|@*" mode="cleanup"/></xsl:copy>
</xsl:template>

<xsl:template match="comment()|@*" mode="cleanup"><xsl:copy/></xsl:template>

<xsl:template match="text()" mode="cleanup"><xsl:copy/></xsl:template>

<xsl:template match="/" mode="cleanup">
	<xsl:copy><xsl:apply-templates select="node()" mode="cleanup" /></xsl:copy>
</xsl:template>

<xsl:template match="*" mode="cleanup">
  <xsl:element name="{local-name()}">
  	<xsl:apply-templates select="node()|@*" mode="cleanup" />
  </xsl:element>
</xsl:template>


<!-- remove PI extensions -->

<xsl:template match="processing-instruction('rfc-ext')" mode="cleanup"/>

<!-- add issues appendix -->

<xsl:template match="back" mode="cleanup">
  <back>
    <xsl:apply-templates select="node()|@*" mode="cleanup" />
    <xsl:if test="not(/*/@ed:suppress-issue-appendix='yes') and //ed:issue[@status='closed']">
      <section title="Resolved issues (to be removed by RFC Editor before publication)">
        <t>
          Issues that were either rejected or resolved in this version of this
          document.
        </t>
        <xsl:apply-templates select="//ed:issue[@status='closed']" mode="issues" />
      </section>
    </xsl:if>
    <xsl:if test="not(/*/@ed:suppress-issue-appendix='yes') and //ed:issue[@status='open']">
      <section title="Open issues (to be removed by RFC Editor prior to publication)">
        <xsl:apply-templates select="//ed:issue[@status!='closed']" mode="issues" />
      </section>
    </xsl:if>
  </back>
</xsl:template>




<!-- extensions -->

<xsl:template match="x:anchor-alias" mode="cleanup"/>

<xsl:template match="x:bcp14" mode="cleanup">
  <xsl:apply-templates/>
</xsl:template>
  
<xsl:template match="x:link" mode="cleanup"/>

<xsl:template match="x:ref" mode="cleanup">
  <xsl:variable name="val" select="."/>
  <xsl:variable name="target" select="//*[@anchor and (@anchor=$val or x:anchor-alias/@value=$val)]"/>
  <xsl:choose>
    <xsl:when test="$target">
      <xref target="{$target/@anchor}" format="none"><xsl:value-of select="."/></xref>
    </xsl:when>
    <xsl:otherwise>
      <xsl:message>WARNING: internal link target for '<xsl:value-of select="."/>' does not exist.</xsl:message>
      <xsl:value-of select="."/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="x:blockquote" mode="cleanup">
  <t><list>
    <xsl:apply-templates mode="cleanup" />
  </list></t>
</xsl:template>

<xsl:template match="x:h" mode="cleanup">
  <xsl:apply-templates mode="cleanup" />
</xsl:template>

<xsl:template match="x:lt" mode="cleanup">
  <t>
    <xsl:apply-templates select="@hangText|@anchor" mode="cleanup"/>
    <xsl:for-each select="t">
      <xsl:apply-templates mode="cleanup"/>
      <xsl:if test="position()!=last()">
        <vspace blankLines="1"/>
      </xsl:if>
    </xsl:for-each>
  </t>
</xsl:template>

<xsl:template match="x:q" mode="cleanup">
  <xsl:text>"</xsl:text>
  <xsl:apply-templates mode="cleanup"/>
  <xsl:text>"</xsl:text>
</xsl:template>

<xsl:template match="x:dfn" mode="cleanup">
  <xsl:apply-templates mode="cleanup"/>
</xsl:template>

<!-- extended reference formatting -->

<xsl:template match="xref[@x:* and not(node())]" mode="cleanup">
  <xsl:choose>
    <xsl:when test="@x:fmt=','">
      <xref>
        <xsl:apply-templates select="@target|@format|@pageno|text()|*" mode="cleanup"/>
      </xref>
      <xsl:text>, Section </xsl:text>
      <xsl:value-of select="@x:sec"/>
    </xsl:when>
    <xsl:when test="@x:fmt='sec'">
      <xsl:text>Section </xsl:text>
      <xsl:value-of select="@x:sec"/>
    </xsl:when>
    <xsl:when test="@x:fmt='number'">
      <xsl:value-of select="@x:sec"/>
    </xsl:when>
    <xsl:when test="@x:fmt='()'">
      <xref>
        <xsl:apply-templates select="@target|@format|@pageno|text()|*" mode="cleanup"/>
      </xref>
      <xsl:text> (Section </xsl:text>
      <xsl:value-of select="@x:sec"/>
      <xsl:text>)</xsl:text>
    </xsl:when>
    <xsl:when test="@x:fmt='of'">
      <xsl:text>Section </xsl:text>
      <xsl:value-of select="@x:sec"/>
      <xsl:text> of </xsl:text>
      <xref>
        <xsl:apply-templates select="@target|@format|@pageno|text()|*" mode="cleanup"/>
      </xref>
    </xsl:when>
    <xsl:when test="@x:fmt='anchor'">
      <xsl:variable name="val">
        <xsl:variable name="target" select="@target" />
        <xsl:variable name="node" select="$src//reference[@anchor=$target]"/>
        <xsl:call-template name="referencename">
          <xsl:with-param name="node" select="$node" />
        </xsl:call-template>
      </xsl:variable>
      <!-- remove brackets -->
      <xsl:value-of select="substring($val,2,string-length($val)-2)"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:copy>
        <xsl:apply-templates select="node()" mode="cleanup"/>
      </xsl:copy>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="xref[@x:fmt and node()]" mode="cleanup">
  <xsl:choose>
    <xsl:when test="@x:fmt='none'">
      <xsl:apply-templates mode="cleanup"/>
    </xsl:when>
    <xsl:when test="not(@x:fmt)">
      <xref>
        <xsl:copy-of select="@target|@format"/>
        <xsl:apply-templates mode="cleanup"/>
      </xref>
    </xsl:when>
    <xsl:otherwise>
      <xsl:message>Unsupported x:fmt attribute.</xsl:message>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!-- issue tracking extensions -->

<xsl:template match="@xml:lang" mode="cleanup"/>
<xsl:template match="@xml:lang" />

<xsl:template match="ed:*" mode="cleanup"/>
<xsl:template match="ed:*" />

<xsl:template match="@ed:*" mode="cleanup"/>
<xsl:template match="@ed:*" />

<xsl:template match="ed:annotation" mode="cleanup" />

<xsl:template match="ed:replace" mode="cleanup">
  <xsl:apply-templates mode="cleanup" />
</xsl:template>

<xsl:template match="ed:replace">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="ed:ins" mode="cleanup">
  <xsl:apply-templates mode="cleanup"/>
</xsl:template>

<xsl:template match="ed:ins">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="ed:issue" mode="issues">
  <section title="{@name}">
    <t>
      Type: <xsl:value-of select="@type" />
    </t>
    <xsl:if test="@href">
      <t>
        <!-- temp. removed because of xml2rfc's handling of erefs when producing TXT-->
        <!--<eref target="{@href}" /> -->
        &lt;<xsl:value-of select="@href"/>>
      </t>
    </xsl:if>
    <xsl:for-each select="ed:item">
      <t>
        <xsl:if test="@entered-by or @date">
          <xsl:choose>
            <xsl:when test="not(@entered-by)">
              <xsl:value-of select="concat('(',@date,') ')" />
            </xsl:when>
            <xsl:when test="not(@date)">
              <xsl:value-of select="concat(@entered-by,': ')" />
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="concat(@entered-by,' (',@date,'): ')" />
            </xsl:otherwise>
          </xsl:choose>      
        </xsl:if>
        <xsl:apply-templates select="node()" mode="issues"/>
      </t>
    </xsl:for-each> 
    <xsl:if test="ed:resolution">
      <t>
        <xsl:text>Resolution</xsl:text>
        <xsl:if test="ed:resolution/@datetime"> (<xsl:value-of select="ed:resolution/@datetime"/>)</xsl:if>
        <xsl:text>: </xsl:text>
        <xsl:value-of select="ed:resolution" />
      </t>
    </xsl:if>
  </section>
</xsl:template>

<xsl:template match="*" mode="issues">
  <xsl:apply-templates mode="issues"/>
</xsl:template>

<xsl:template match="xhtml:br" mode="issues">
  <vspace/>
</xsl:template>

<xsl:template match="xhtml:del" mode="issues">
  <xsl:text>&lt;del></xsl:text>
    <xsl:apply-templates mode="issues"/>
  <xsl:text>&lt;/del></xsl:text>
</xsl:template>

<xsl:template match="xhtml:em" mode="issues">
  <spanx style="emph">
    <xsl:apply-templates mode="issues"/>
  </spanx>
</xsl:template>

<xsl:template match="xhtml:ins" mode="issues">
  <xsl:text>&lt;ins></xsl:text>
    <xsl:apply-templates mode="issues"/>
  <xsl:text>&lt;/ins></xsl:text>
</xsl:template>

<xsl:template match="text()" mode="issues">
  <xsl:value-of select="." />
</xsl:template>



<!-- markup inside artwork element -->

<xsl:template match="figure[.//artwork//iref]" mode="cleanup">
  <!-- move up iref elements -->
  <figure>
    <xsl:apply-templates select="@*" mode="cleanup" />
    <xsl:apply-templates select=".//artwork//iref" mode="cleanup"/>
    <xsl:apply-templates select="iref|preamble|artwork|postamble" mode="cleanup" />
  </figure>
</xsl:template>

<xsl:template match="artwork" mode="cleanup">
  <xsl:variable name="content"><xsl:apply-templates select="."/></xsl:variable>
  <artwork>
    <xsl:apply-templates select="@*" mode="cleanup" />
    <xsl:if test="starts-with(.,'&#10;')">
      <xsl:text>&#10;</xsl:text>
    </xsl:if>
    <xsl:value-of select="translate($content,'&#160;&#x2500;&#x2502;&#x2508;&#x250c;&#x2510;&#x2514;&#x2518;&#x251c;&#x2524;',' -|+++++++')"/>
  </artwork>  
</xsl:template>



<!-- artwork extensions -->
<xsl:template match="artwork/@x:extraction-note" mode="cleanup"/>

<!-- referencing extensions -->
<xsl:template match="iref/@x:for-anchor" mode="cleanup"/>

<!-- table styles -->
<xsl:template match="texttable/@style" mode="cleanup"/>

<!-- anchor extensions -->
<xsl:template match="preamble/@anchor" mode="cleanup"/>


</xsl:transform>