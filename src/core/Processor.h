/*
Copyright (c) 2003-2010 Sony Pictures Imageworks Inc., et al.
All Rights Reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name of Sony Pictures Imageworks nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/


#ifndef INCLUDED_OCS_PROCESSOR_H
#define INCLUDED_OCS_PROCESSOR_H

#include <OpenColorSpace/OpenColorSpace.h>

#include "Op.h"

OCS_NAMESPACE_ENTER
{

    // TODO: hide constructor, add create function?
    // TODO: use custom delete?
    
    class OCSProcessor : public Processor
    {
    public:
        OCSProcessor(const OpRcPtrVec& opVec);
        
        virtual ~OCSProcessor();
        
        virtual bool isNoOp() const;
        
        virtual void render(ImageDesc& img) const;
        
        virtual const char * getHWShaderText(const HwProfileDesc & hwDesc) const;
        virtual int getHWLut3DEdgeSize() const;
        virtual const char * getHWLut3DCacheID(const HwProfileDesc & hwDesc) const;
        virtual void getHWLut3D(float* lut3d, const HwProfileDesc & hwDesc) const;
        
    private:
        OpRcPtrVec m_opVec;
    };
    
    
}
OCS_NAMESPACE_EXIT

#endif